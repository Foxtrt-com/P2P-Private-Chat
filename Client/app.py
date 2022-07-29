# /app.py

from os.path import exists

from modules.config_parser import Config
from modules.message_handler import *
from modules.encryption import RSA
from modules.gui import *


def main():
    """
    Main program start code

    :return: None
    """

    print("> Checking Config.ini")
    config = Config()
    if exists('config.ini'):
        config.read('config.ini')
    else:
        print("> Config.ini not found. Creating with default settings and new RSA keypair")

        config.display_name = "User"
        config.theme = "Dark"
        config.rendezvous_server = "server.example.com"
        config.rendezvous_port = 5000

        rsa = RSA()

        config.public_key = rsa.public_key
        config.private_key = rsa.private_key

        config.save('config.ini')

    try:
        print("> Creating Message Handler")

        with Handler(config) as message_handler:
            while True:
                try:
                    message_handler.send(input(''))
                except ConnectionResetError:
                    continue
    except socket.gaierror as e:
        print("Error: Server Not Found")
        print(e)


if __name__ == '__main__':
    print("""
############################################
#        P2P Private Chat - Client         #
#           Copyright Foxtrt.com           #
#                                          #
#  github.com/Foxtrt-com/P2P-Private-Chat  #
############################################""")

    gui = GUI("Dark")
    gui.mainloop()
    main()
