class Effect:
    def __init__(self, target, termination):
        self._target = target
        self._termination = termination

    def trigger(self):
        pass

    def terminate(self):
        pass
