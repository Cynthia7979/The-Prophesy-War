class Effect:
    def __init__(self, target, effect):
        self.target = target
        self.effect = effect

    def pack(self):
        return "{target}|{effect}"

def unpack(s: str):
    try:
        target, effect = s.split("|")
        return Effect(target, effect)
    expect:
        print("Wrong string for unpack")
