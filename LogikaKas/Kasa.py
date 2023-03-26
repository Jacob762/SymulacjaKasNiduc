from LogikaKas.Klient import Klient


class Kasa:

    def __init__(self, idKasy: int, maxCapacity: int):
        self.idKasy = idKasy
        self.active = False
        self.iloscTransakcji = 0
        self.wolna = False
        self.klienci = []
        self.maxCapacity = maxCapacity
        self.straznik = Klient
        self.straznik.czasObslugi = 0
        self.obslugiwany = self.straznik
        self.ilePusta = 0  # okresla ile "rund" kasa stoi pusta, po x rundach zamyka kase

    def getIloscTransakcji(self):
        return self.iloscTransakcji

    def getActive(self):
        return self.active

    def getWolna(self):
        return self.wolna

    def getKlienci(self):
        return self.klienci

    def getSize(self):
        return len(self.klienci)

    def getId(self):
        return self.idKasy

    def getIlePusta(self):
        return self.ilePusta

    def dodajKlienta(self, klient: Klient):
        if self.getSize() < self.maxCapacity:
            self.klienci.append(klient)
            return 1
        else:
            return -7

    def obsluzKlienta(self):
        if not self.getActive(): return -7
        if self.obslugiwany.czasObslugi == 0 and len(self.klienci) > 0:
            self.obslugiwany = self.klienci.pop(0) #zabezpieczyc przed popowaniem z pustej listy
            self.obslugiwany.czasObslugi -=1
            self.ilePusta = 0
            self.iloscTransakcji += 1
        elif self.obslugiwany.czasObslugi == 0:
            self.obslugiwany = self.straznik # straznik oznacza ze nikt nie stoi przy kasie
            self.ilePusta += 1
        else:
            self.obslugiwany.czasObslugi -= 1

    def otworzKase(self):
        self.active = True

    def zamknijKase(self):
        self.active = False
        self.ilePusta = 0
