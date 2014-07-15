import configparser

CONF_FILE_NAME = 'brickowl2rebrickable.ini'


def _get_config():
    config = configparser.ConfigParser()
    config.read(CONF_FILE_NAME)
    return config


def get_brickowl_api_key():
    try:
        return _get_config()['DEFAULT']['BrickOwlApiKey']
    except KeyError:
        return None


def get_rebrickable_api_key():
    try:
        return _get_config()['DEFAULT']['RebrickableApiKey']
    except KeyError:
        return None