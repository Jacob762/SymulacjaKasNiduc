from LogikaKas.Klient import Klient


class Kasa:

    def __init__(self, idKasy: int, maxCapacity: int):
        self.idKasy = idKasy
        self.serwis = 0
        self.wypadek = False
        self.stopTime = 0
        self.active = False
        self.iloscTransakcji = 0
        self.awaria = False
        self.klienci = []
        self.maxCapacity = maxCapacity
        self.straznik = Klient  # stoi przy kasie jak jest pusta, tymczasowe rozwiazanie
        self.straznik.czasObslugi = 0
        self.obslugiwany = self.straznik
        self.obsluga = False
        self.ilePusta = 0  # okresla ile "rund" kasa stoi pusta, po x rundach zamyka kase
        self.ilePieniedzy=2_000

    def getIloscTransakcji(self):
        # if self.active:
        return self.iloscTransakcji

    def getActive(self):
        return self.active

    def setActive(self, wartosc: bool):
        self.active = wartosc

    def getstopTime(self):
        return self.stopTime

    def getObsluga(self):
        return self.obsluga

    def setstopTime(self, wartosc: int):
        self.setActive(False)
        self.wypadek = True
        self.stopTime += wartosc

    def resetstopTime(self):
        self.setActive(True)
        self.wypadek = False
        self.stopTime = 0

    def getWypadek(self):
        return self.wypadek

    def getAwaria(self):
        return self.awaria

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

    def dodajPieniadze(self, cash: int):
        if self.ilePieniedzy<10_000:
            self.ilePieniedzy += cash
            return 1
        else:
            return -8

    # plan był taki żeby wyw
    #


    def awariaStart(self, czasSerwisowania: int):
        self.awaria = True
        self.serwis = czasSerwisowania
        self.iloscTransakcji = 0

    def awariaStop(self):
        self.awaria = False
        self.serwis = 0
        self.iloscTransakcji = 0

    def obsluzKlienta(self):
        if not self.getActive(): return -7
        if self.obslugiwany.czasObslugi == 0 and len(self.klienci) > 0:
            self.obsluga = True
            if len(self.klienci)>0:
                self.obslugiwany = self.klienci.pop(0)  # zabezpieczyc przed popowaniem z pustej listy -> Done :))
                self.obslugiwany.czasObslugi -= 1
                self.ilePusta = 0
                self.iloscTransakcji += 1
        elif self.obslugiwany.czasObslugi == 0:
            self.obsluga = False
            self.obslugiwany = self.straznik  # straznik oznacza ze nikt nie stoi przy kasie
            self.ilePusta += 1
        else:
            self.obslugiwany.czasObslugi -= 1

    def otworzKase(self):
        self.active = True

    def zamknijKase(self, kolejka):
        if len(self.klienci) > 0:
            while len(self.klienci) > 0:
                kolejka.append(self.klienci.pop(0))
        self.active = False
        self.ilePusta = 0