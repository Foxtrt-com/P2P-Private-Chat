# /modules/encryption.py
"""
RSA & AES Encryption and key generation
"""

import rsa
import rsa.randnum
from Crypto.Cipher import AES as aes


class RSA:
    def __init__(self, public_key=None, private_key=None):
        """
        Contains methods to encrypt, decrypt and generate new key pairs

        :param public_key: Existing Public Key
        :param private_key: Existing Private Key
        """
        self.public_key = public_key
        self.private_key = private_key

        if public_key is None or private_key is None:
            # If no public or private keys are given, generate new ones automatically
            self.generate()

    def generate(self):
        """
        Sets the public and private keys using RSA to generate new keys

        :return: public_key, private_key
        """
        public_key, private_key = rsa.newkeys(2048)
        self.public_key = str(public_key)
        self.private_key = str(private_key)
        return self.public_key, self.private_key

    def encrypt(self, value, public_key):
        """
        Encrypts the given value using the given public key

        :param value: Value to encrypt
        :param public_key: Public key to use
        :return: Encrypted value
        """
        key_string = public_key.strip("PublicKey(").strip(")")
        n, e = key_string.split(", ", 1)
        public_key = rsa.PublicKey(int(n), int(e))

        return rsa.encrypt(value, public_key)

    def decrypt(self, value):
        key_string = self.private_key.strip("PrivateKey(").strip(")")
        n, e, d, p, q = key_string.split(", ", 4)
        private_key = rsa.PrivateKey(int(n), int(e), int(d), int(p), int(q))

        return rsa.decrypt(value, private_key)


class AES:
    def __init__(self):
        """
            Contains methods to encrypt, decrypt using AES ciphers
        """

    def encrypt(self, value):
        """
        Applies a cipher using a generated AES key

        :param value: Value to apply the cipher to
        :return: Cipher text, AES key, nonce
        """
        key = rsa.randnum.read_random_bits(256)

        cipher = aes.new(key, aes.MODE_EAX)

        ciphertext, _ = cipher.encrypt_and_digest(value.encode())
        nonce = cipher.nonce

        return ciphertext, key, nonce

    def decrypt(self, value, key, nonce):
        """
        Removes a cipher using the given AES key and nonce

        :param value: value to decrypt
        :param key: AES key
        :param nonce: Nonce
        :return: Plain text
        """

        cipher = aes.new(key, aes.MODE_EAX, nonce=nonce)

        plaintext = cipher.decrypt(value).decode()

        return plaintext
