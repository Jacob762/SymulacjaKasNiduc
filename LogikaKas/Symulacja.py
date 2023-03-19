from LogikaKas.Kasa import Kasa


class Simulation:
    lista = []

    def __init__(self):
        self.start()

    def start(self):
        print("Simulation begins")
        self.addKasa()

    def addKasa(self):
        self.lista.append(Kasa(1000, True))

    def queueFull(self, kasa: Kasa):
        if kasa.getPeople() == 10:
            return True
        else:
            return False
