# /modules/config_parser.py
"""
Reads and Writes config files
"""

from configparser import ConfigParser


class Config:
    def __init__(self):
        """
        Contains methods to read and save configuration files
        """
        self.display_name = None
        self.theme = None
        self.rendezvous_server = None
        self.rendezvous_port = None
        self.public_key = None
        self.private_key = None

    def read(self, config_file):
        """
        Reads a file for the configuration variables

        :param config_file: relative or full path of config file
        :return: Config object
        """
        config = ConfigParser()
        config.read(config_file)

        self.display_name = config.get('client', 'display_name')
        self.theme = config.get('client', 'theme')
        self.rendezvous_server = config.get('client', 'rendezvous_server')
        self.rendezvous_port = config.getint('client', 'rendezvous_port')
        self.public_key = config.get('client', 'public_key')
        self.private_key = config.get('client', 'private_key')

        return self

    def save(self, config_file):
        """
        Saves a file with the configuration variables

        :param config_file: relative or full path of config file
        :return: Config object
        """
        config = ConfigParser()
        config.add_section('client')
        config['client']['display_name'] = self.display_name
        config['client']['theme'] = self.theme
        config['client']['rendezvous_server'] = self.rendezvous_server
        config['client']['rendezvous_port'] = str(self.rendezvous_port)
        config['client']['public_key'] = str(self.public_key)
        config['client']['private_key'] = str(self.private_key)

        with open(config_file, 'w') as file:
            config.write(file)

        return self
