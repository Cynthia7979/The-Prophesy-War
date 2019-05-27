# Working directory: The-Prophesy-War/Python/client/
import json
import sys, os
import components.logger as logger

LOGGER = logger.get_public_logger('JSON_Editor')
SETTING_FILE = 'settings.json'
DEFAULT = {'settings': {'resolution': (1080, 720), 'language': 'zh'}}


def update_settings(s):
    """
    Update settings.json.
    :param s: Complete settings dict to save.
    """
    data['settings'] = s
    with open(SETTING_FILE, 'w') as f:
        json.dump(s, f)
    LOGGER.info('settings.json was updated to {}.'.format(s))


def get_settings(key=None, keys=None):
    """
    Get all settings, or the specific one(s) given.
    :param key: Indicate which entry to return. Default None.
    :param keys: Indicate which entries to return. Default None.
    :return: Dict of all settings if no key specified.
             String of an entry if :param key: given.
             Dict of specified entries if :param keys: given.
    """
    result = {}
    if keys:
        for k in keys:
            try:
                result[k] = data['settings'][k]
            except KeyError:
                result[k] = DEFAULT['settings'][k]
        return result
    elif key:
        try:
            return data['settings'][key]
        except KeyError:
            return DEFAULT['settings'][key]
    else:
        return data['settings']


def main():
    global data
    data = {}
    try:
        with open(SETTING_FILE) as f:
            data['settings'] = json.load(f)
    except json.decoder.JSONDecodeError:
        LOGGER.warning('No data in settings.json')
        data = DEFAULT
        with open(SETTING_FILE, 'w') as f:
            json.dump(data['settings'], f)


def close():
    sys.exit()


main()
