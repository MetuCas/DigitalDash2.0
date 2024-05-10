# config_utils.py

import configparser

def read_config(section, key):
    config = configparser.ConfigParser()
    config.read('config.txt')
    value = config.get(section, key)
    print(f"Reading config: {section} {key} = {value}")  # Debug output
    return value
