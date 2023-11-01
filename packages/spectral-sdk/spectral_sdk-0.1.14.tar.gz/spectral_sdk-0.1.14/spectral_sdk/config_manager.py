import configparser
import os


class ConfigManager:
    def __init__(self, config_path):
        self.config_path = os.path.expanduser(config_path)
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        self.config.read(self.config_path)

    def save_config(self):
        with open(self.config_path, "w") as f:
            self.config.write(f)

    def set(self, section, key, value):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self.save_config()

    def get(self, section, key):
        return self.config.get(section, key, fallback=None)
