# config_utils.py

import configparser

def read_config(section, key):
    config = configparser.ConfigParser()
    config.read('config.txt')
    return config.get(section, key)
