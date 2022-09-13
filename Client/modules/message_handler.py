# /modules/message_handler.py

from .encryption import AES, RSA
from .connections import Connections
from .gui import *

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
        self.inbound_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.inbound_socket.bind(('0.0.0.0', 0))
        self.outbound_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.outbound_socket.bind(('0.0.0.0', 0))
        self.connected = False
        self.listener = None
        self.gui = GUI(self, self.config)

    def start(self):
        self.connect_to_rendezvous()
        self.start_listener()

        self.gui.mainloop()

        self.send_disconnect()
        self.listener.join()
        self.inbound_socket.shutdown(1)
        self.outbound_socket.shutdown(1)

    def send(self, message):
        print("> Sending message to peers")

        for peer in self.peers.list_of_peers():
            # Encrypt with AES
            cipher_text, key, nonce = self.aes.encrypt(json.dumps(message))
            # Encrypt AES Key with RSA
            encrypted_key = self.rsa.encrypt(key, peer['public_key'])

            # Send data to peer
            self.outbound_socket.sendto(encrypted_key + nonce + cipher_text, (peer['address'], peer['inbound_port']))

    def connect_to_rendezvous(self):
        print("> Sending connect message to rendezvous")
        self.outbound_socket.sendto(f"CONNECT-{self.config.display_name}-{self.config.public_key}-"
                                    f"{self.inbound_socket.getsockname()[1]}".encode(), self.rendezvous)

        print("> Receiving peer list from rendezvous")
        data, address = self.outbound_socket.recvfrom(65536)
        recv = {"key": data[:256], "nonce": data[256:272], "data": data[272:]}

        key = self.rsa.decrypt(recv["key"])
        peers = json.loads(self.aes.decrypt(recv["data"], key, recv["nonce"]))

        self.connected = True
        for peer in peers:
            self.peers.add(peer)
            self.gui.peer_list.insert(END, peer['display_name'])

        if len(self.peers) >= 1:
            print("> Sending connect message to peers")
            self.send(f"CONNECT-{self.config.display_name}-{self.config.public_key}-"
                      f"{self.inbound_socket.getsockname()[1]}")

    def send_disconnect(self):
        print("> Sending disconnect message to peers and rendezvous")
        self.send(f"DISCONNECT-{self.config.display_name}-{self.config.public_key}-"
                  f"{self.inbound_socket.getsockname()[1]}")
        self.outbound_socket.sendto(f"DISCONNECT-{self.config.display_name}-{self.config.public_key}-"
                                    f"{self.inbound_socket.getsockname()[1]}".encode(), self.rendezvous)
        self.connected = False

    def receive(self):
        while self.connected:
            data, address = self.inbound_socket.recvfrom(65536)
            recv = {"key": data[:256], "nonce": data[256:272], "data": data[272:]}
            key = self.rsa.decrypt(recv["key"])
            text = json.loads(self.aes.decrypt(recv["data"], key, recv["nonce"]))

            if text.startswith("CONNECT-"):
                print(f"> New connection from {address}")
                _, display_name, public_key, inbound_port = text.split("-")
                ip, outbound_port = address
                self.peers.add({'display_name': display_name, 'public_key': public_key, 'address': ip,
                                'inbound_port': int(inbound_port), 'outbound_port': outbound_port})
                self.gui.peer_list.insert(END, display_name)
            elif text.startswith("DISCONNECT-"):
                print(f"Existing peer disconnected {address}")
                _, display_name, public_key, inbound_port = text.split("-")
                ip, outbound_port = address
                self.peers.sub({'display_name': display_name, 'public_key': public_key, 'address': ip,
                                'inbound_port': int(inbound_port), 'outbound_port': outbound_port})
                index = self.gui.peer_list.get(0, tk.END).index(display_name)
                self.gui.peer_list.delete(index)
            else:
                peer_name = None
                for peer in self.peers.list_of_peers():
                    if (peer['address'], peer['outbound_port']) == address:
                        peer_name = peer['display_name']

                self.gui.message_list.insert(END, f"{peer_name}: {text}")

    def start_listener(self):
        print("> Starting listener")

        self.listener = threading.Thread(target=self.receive, args=())
        self.listener.start()
