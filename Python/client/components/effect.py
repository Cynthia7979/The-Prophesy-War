"""
Card Effects.
Still don't know how to format the complex effects... TODO
"""
import logger
import re

string_code = {''}


class Effect:
    """Card Effects"""
    def __init__(self, target, code):
        """
        Returns an `Effect` object
        :param target: Target of the effect
        :param code: Effect code TODO
        """
        self.target = target
        self.code = code


def unpack(s: str):
    """
    Unpacks effect from string
    :param s: Effect code TODO
    :return: `Effect` object
    """
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
