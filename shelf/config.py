import configparser
import os


class config:
    def __init__(self, config_file: str) -> None:

        if not os.path.isfile(config_file):
            raise Exception(f"File {config_file} not found, exit!")

        parser = configparser.ConfigParser()
        with open(config_file) as file:
            parser.read_file(file)
