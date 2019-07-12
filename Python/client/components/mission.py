class Mission(object):
    def __init__(self, description, difficulty:int):
        self.description = description
        self._countdown = 2
        self.award = {'coin': difficulty*20+50, 'fame': difficulty*5+10}
        self.punishment = {'coin': -30, 'fame': -10}

    def countdown(self):
        self._countdown -= 1

    def accept(self):
        self._countdown = 3

    def expired(self):
        return self._countdown <= 0
