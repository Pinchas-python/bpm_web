import os
import configparser
from pathlib import Path

configuration = {}
slas = {}

path = Path(__file__).parent


def init_config(config_path):
    config = configparser.ConfigParser()
    if config_path:
        config.read(config_path)
    else:
        config_file_path = os.path.join(path, "../../config.ini")
        config.read(config_file_path)
    config_selctions_list = config.sections()
    for config_section in config_selctions_list:
        for key in config[config_section]:
            configuration[key] = config[config_section][key]