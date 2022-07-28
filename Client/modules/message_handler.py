# /modules/message_handler.py

from .encryption import AES, RSA
from .connections import Connections

import socket
import json
import threading


class Handler:
    def __init__(self, config):
        self.config = config
        self.rendezvous = (config.rendezvous_server, config.rendezvous_port)
        self.peers = Connections()
        self.aes = AES()
        self.rsa = RSA(config.public_key, config.private_key)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', 0))
        self.connected = False
        self.listener = None

    def __enter__(self):
        self.connect_to_rendezvous()

        self.start_listener()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.send_disconnect()
        self.listener.join()
        self.socket.shutdown(1)

    def send(self, message):
        print("> Sending message to peers")

        for peer in self.peers.list_of_peers():
            # Encrypt with AES
            cipher_text, key, nonce = self.aes.encrypt(json.dumps(message))
            # Encrypt AES Key with RSA
            encrypted_key = self.rsa.encrypt(key, peer['public_key'])

            # Send data to peer
            self.socket.sendto(encrypted_key + nonce + cipher_text, tuple(peer['address']))

    def connect_to_rendezvous(self):
        print("> Sending connect message to rendezvous")
        self.socket.sendto(f"CONNECT-{self.config.display_name}-{self.config.public_key}".encode(), self.rendezvous)

        print("> Receiving peer list from rendezvous")
        data, address = self.socket.recvfrom(65536)
        recv = {"key": data[:256], "nonce": data[256:272], "data": data[272:]}

        key = self.rsa.decrypt(recv["key"])
        peers = json.loads(self.aes.decrypt(recv["data"], key, recv["nonce"]))

        self.connected = True

        for peer in peers:
            self.peers.add(peer)

        if len(self.peers) >= 1:
            print("> Sending connect message to peers")
            self.send(f"CONNECT-{self.config.display_name}-{self.config.public_key}")

    def send_disconnect(self):
        print("> Sending disconnect message to peers and rendezvous")
        self.send(f"DISCONNECT-{self.config.display_name}-{self.config.public_key}")
        self.socket.sendto(f"DISCONNECT-{self.config.display_name}-{self.config.public_key}".encode(), self.rendezvous)
        self.connected = False

    def receive(self):
        while self.connected:
            data, address = self.socket.recvfrom(65536)
            recv = {"key": data[:256], "nonce": data[256:272], "data": data[272:]}
            key = self.rsa.decrypt(recv["key"])
            text = json.loads(self.aes.decrypt(recv["data"], key, recv["nonce"]))

            if text.startswith("CONNECT-"):
                print(f"> New connection from {address}")
                _, display_name, public_key = text.split("-")
                self.peers.add({'display_name': display_name, 'public_key': public_key, 'address': address})
            elif text.startswith("DISCONNECT-"):
                print(f"Existing peer disconnected {address}")
                _, display_name, public_key = text.split("-")
                self.peers.sub({'display_name': display_name, 'public_key': public_key, 'address': address})
            else:
                peer_name = None
                for peer in self.peers.list_of_peers():
                    if tuple(peer['address']) == address:
                        peer_name = peer['display_name']

                print(f"{peer_name}: {text}")

    def start_listener(self):
        print("> Starting listener")

        self.listener = threading.Thread(target=self.receive, args=())
        self.listener.start()
