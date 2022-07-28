# /modules/message_handler.py

from .encryption import AES, RSA
from .connections import Connections

import socket
import json


class Handler:
    def __init__(self, config):
        self.config = config
        self.peers = Connections()
        self.aes = AES()
        self.rsa = RSA()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', config.rendezvous_port))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.shutdown(1)

    def send(self, message, peer):
        # Encrypt with AES
        cipher_text, key, nonce = self.aes.encrypt(json.dumps(message))
        # Encrypt AES Key with RSA
        encrypted_key = self.rsa.encrypt(key, peer['public_key'])

        print("> Sending new peer a list of current peers")

        # Send data to peer
        self.socket.sendto(encrypted_key + nonce + cipher_text, peer['address'])

    def receive(self):
        while True:
            data, address = self.socket.recvfrom(65536)
            text = data.decode()

            if text.startswith("CONNECT-"):
                print(f"> New connection from {address}")
                _, display_name, public_key = text.split("-")

                self.send(self.peers.peers, {'display_name': display_name, 'public_key': public_key, 'address': address})
                self.peers.add({'display_name': display_name, 'public_key': public_key, 'address': address})
            elif text.startswith("DISCONNECT-"):
                print(f"> Existing peer disconnected {address}")
                _, display_name, public_key = text.split("-")
                self.peers.sub({'display_name': display_name, 'public_key': public_key, 'address': address})

    def start_listener(self):
        self.receive()
