"""
Json file editor. Handler for json library.

**NOTE:** `data` is globalized in `main()`!
"""
# Working directory: The-Prophesy-War/Python/client/
import json
import sys, os
if os.path.basename(os.getcwd()) == 'client':
    os.chdir('components/')
from . import logger  # I will try to change this... if possible


os.chdir('../')  # To Python/client (the Universe and Beyond!x)
LOGGER = logger.get_public_logger('JSON_Editor')  # Logger for the file
SETTING_FILE = 'settings.json'  # User preference
SETTING_LIST_FILE = 'settings_list.json'  # How the in-game preference window is displayed
DEFAULT = {'settings': {'resolution': (1080, 720), 'language': 'zh'}}  # Default setting to use when no preference file
#                                                                        is found. TODO I should make this a file


def update_settings(s: dict):
    """
    Update settings.json.
    :param s: Complete settings dict to save. e.g. Something that resembles DEFAULT
    """
    data['settings'] = s
    with open(SETTING_FILE, 'w') as f:
        json.dump(s, f)  # Dump s into f
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
    if keys:  # If multiple entries are specified,
        for k in keys:  # For each entry,
            try:
                result[k] = data['settings'][k]  # Get the value of that entry.
            except KeyError:  # If this entry isn't set,
                result[k] = DEFAULT['settings'][k]  # Return the default value.
        return result
    elif key:  # If only one entry is specified,
        try:  # Same process.
            return data['settings'][key]
        except KeyError:
            return DEFAULT['settings'][key]
    else:
        return data['settings']  # Return all data when no entry is specified.


def get_settings_list():
    with open(SETTING_LIST_FILE, encoding="UTF-8") as sl:
        return json.load(sl, encoding="UTF-8")


def main():
    global data
    data = {}  # Current setting data
    try:
        with open(SETTING_FILE) as f:
            data['settings'] = json.load(f)
    except json.decoder.JSONDecodeError:
        LOGGER.warning('No data in settings.json')  # Usually when the game is open for the first time.
        data = DEFAULT
        with open(SETTING_FILE, 'w') as f:
            json.dump(data['settings'], f)  # Write default data


def close():
    sys.exit()


main()
