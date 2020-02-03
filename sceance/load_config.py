import configparser

THIS_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
SETTINGS_FILE = "settings.ini"

config.read(THIS_DIRECTORY+SETTINGS_FILE)
