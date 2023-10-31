# settings.py

import configparser


def initialize_settings():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    return config['API']['key']
