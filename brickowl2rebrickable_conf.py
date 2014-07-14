import configparser

CONF_FILE_NAME = 'brickowl2rebrickable.ini'

def get_config():
    config = configparser.ConfigParser()
    config.read(CONF_FILE_NAME)
    return config

def get_brickowl_api_key():
    try:
        return get_config()['DEFAULT']['BrickOwlApiKey']
    except KeyError:
        return None


