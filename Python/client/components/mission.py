"""
Mission (or "quest") class.
"""


class Mission(object):
    def __init__(self, description, difficulty:int):
        self.description = description
        self._countdown = 2  # A mission can only be accepted in 2 rounds before it disappear
        self.award = {'coin': difficulty*20+50, 'fame': difficulty*5+10}
        self.punishment = {'coin': -30, 'fame': -10}

    def countdown(self):
        """Call this method once every round"""
        self._countdown -= 1

    def accept(self):
        """Call this method if mission is accepted"""
        self._countdown = 3  # A mission must be done in 3 rounds

    def expired(self):
        """
        Check if the mission has expired (whether from accomplishing or accepting)
        :return: bool value
        """
        return self._countdown <= 0
