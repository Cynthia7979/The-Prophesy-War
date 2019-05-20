import json
import sys, os
import components.logger as logger

LOGGER = logger.get_public_logger('JSON_Editor')


def check_lock(func):
    def lock_wrapper(*args, **kwargs):
        while lock:
            pass
        return func(args, kwargs)
    return lock_wrapper


@check_lock
def update_settings(setting):
    data['settings'] = setting
    with open('../settings.json', 'w') as f:
        json.dump(setting, f)


@check_lock
def get_settings(key=None, keys=None):
    result = {}
    if keys:
        for key in keys:
            result[key] = data['settings'][key]
        return result
    elif key:
        return data['settings'][key]
    else:
        return data['settings']


def main():
    global data, lock
    data = {}
    lock = True
    try:
        with open('../settings.json') as f:
            data['settings'] = json.load(f)
    except json.decoder.JSONDecodeError:
        LOGGER.warning('No data in settings.json')
        data = {'settings': {'resolution': (1080, 720)}}
        with open('../settings.json', 'w') as f:
            json.dump(data['settings'], f)
    lock = False


def close():
    sys.exit()


main()
