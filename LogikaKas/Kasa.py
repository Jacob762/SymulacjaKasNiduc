class Kasa:
    def __init__(self, valCash: float, active: bool, people: int):
        self.active = active
        self.valCash = valCash
        self.people = people

    def getVal(self):
        return self.valCash

    def getActive(self):
        return self.active

    def setBroke(self):
        self.active = False

    def getPeople(self):
        return self.people



