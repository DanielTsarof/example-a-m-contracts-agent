import yaml

from constants import CONFIG_PATH
from utils.config_class import Config

config = Config(**(yaml.safe_load(CONFIG_PATH.read_text()) or {}))
