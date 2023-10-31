# settings.py
import os
import configparser


def initialize_settings():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    config_path = os.path.join(parent_directory, 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['API']['key']
