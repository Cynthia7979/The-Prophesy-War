class Effect:
    def __init__(self, target, effect):
        self.target = target
        self.effect = effect

    def pack(self):
        return "{target}|{effect}"
