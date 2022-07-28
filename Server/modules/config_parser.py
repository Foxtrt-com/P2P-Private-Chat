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
        self.rendezvous_port = None

    def read(self, config_file):
        """
        Reads a file for the configuration variables

        :param config_file: relative or full path of config file
        :return: Config object
        """
        config = ConfigParser()
        config.read(config_file)

        self.rendezvous_port = config.getint('server', 'rendezvous_port')

        return self

    def save(self, config_file):
        """
        Saves a file with the configuration variables

        :param config_file: relative or full path of config file
        :return: Config object
        """
        config = ConfigParser()
        config.add_section('server')
        config['server']['rendezvous_port'] = str(self.rendezvous_port)

        with open(config_file, 'w') as file:
            config.write(file)

        return self
