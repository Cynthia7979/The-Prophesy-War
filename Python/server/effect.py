import logger
import re

string_code = {''}


class Effect:
    def __init__(self, target, code):
        self.target = target
        self.code = code


def unpack(s: str):
    try:
        target, name, effect = s.split('|', 2)
        code = """"""
        try:
            found = re.search('\[(.*)123]', s).group(1)
            unpack(found)
        except AttributeError:
            pass

    except ValueError:
        print("Wrong string for unpack")
