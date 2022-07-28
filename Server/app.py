# /app.py

from os.path import exists

from modules.config_parser import Config
from modules.message_handler import *


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
        print("> Config.ini not found. Creating with default port 5000")
        config.rendezvous_port = 5000
        config.save('config.ini')

    print("> Creating Message Handler")
    message_handler = Handler(config)

    print(f"> Starting listener on port {config.rendezvous_port}")
    message_handler.start_listener()

    print("> Program shutdown")


if __name__ == '__main__':
    print("""
############################################
#        P2P Private Chat - Server         #
#           Copyright Foxtrt.com           #
#                                          #
#  github.com/Foxtrt-com/P2P-Private-Chat  #
############################################""")
    main()
