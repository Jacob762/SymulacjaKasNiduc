import random

from LogikaKas.Kasa import Kasa
from LogikaKas.Klient import Klient


class Simulation:
    lista = []
    klientela = []
    lastCall = False  # zmienna do okreslania ostatnich 20 minut w sklepie
    # atrybuty poczatkowe
    maxIloscTransakcji = 30
    czasSerwisowania = 10
    # statystyki dotyczące klientów
    # statystyki ogólne 
    klienciWszyscy = 0
    klienciKarta = 0
    klienciPlastik = 0
    klienciAplikacja = 0  # w sumie to można usunąc i na koniec odjąc od tych z kartą tych z plastikiem
    klienciPolacy = 0

    # statystyki dzienne + godzinowe bedą w odpowiedniej pętli

    def __init__(self, iloscKas: int):
        self.start(iloscKas)
        self.simulatione(1, 12)

    # Dodaje ilosc kas po czym inicjalizuje pierwszą kase:
    def start(self, iloscKas: int):
        print("Simulation begins")
        for i in range(iloscKas):
            self.addKasa(i + 1)
        self.lista[0].active = True

    def addKasa(self, index: int):
        self.lista.append(Kasa(index, 8))

    def simulatione(self, dniPracy: int, godzinyPracy):
        for dzien in range(dniPracy):
            self.lastCall = False
            # statysyki dzienne
            print(f"DZIEN {dzien}")
            for godziny in range(godzinyPracy):
                # statystyki godzinowe
                for i in range(60):
                    print(f"{i + 1},  ITERACJA")
                    # ostatnie 20 minut przed klienci nie przychodza
                    if godzinyPracy - godziny == 1 and i == 40:
                        self.lastCall = True
                    # dodwanie klientow do ogolnej kolejki
                    if not self.lastCall:
                        self.generujKlienta()

                    print(f"{len(self.klientela)} DLUGOSC KLIENELI")
                    # petla do dyspozycji nowych klientow
                    j = 0
                    # szukamy pierwszej aktywnej kasy
                    while j < len(self.lista):
                        if self.lista[j].getActive():
                            break
                        else:
                            j += 1
                    if j == len(self.lista): j = 0
                    # dodaje do pierwszej z brzegu zamiast zaczynac od aktywnych (to-do)
                    while len(self.klientela) > 0 and j < len(self.lista):
                        if self.lista[j].dodajKlienta(self.klientela.pop(0)) == -7:
                            j += 1
                        elif not self.lista[j].getActive():
                            self.lista[j].setActive(True)

                    for k in range(len(self.lista)):
                        print(f"{len(self.lista[k].klienci)},  ZAPELNIENIE KASY")
                        print(f"CZAS OCZEKIWANIA NA KONIEC WYPADKU: {self.lista[k].stopTime}")


                    if len(self.klientela) != 0:
                        print("Wszystkie kasy zajete")

                    for k in range(len(self.lista)):
                        # trzeba dodac zeby tylko aktywne kasy obslugiwaly klientow
                        if self.lista[k].getstopTime() == 0 and self.lista[k].getWypadek():
                            self.lista[k].resetstopTime()
                        elif self.lista[k].getstopTime() != 0:
                            self.lista[k].stopTime -= 1
                        # sprawdza czy kasa osiagnela maksymalna ilosc transkacji
                        if self.lista[k].getActive():
                            if self.lista[k].getIloscTransakcji() == self.maxIloscTransakcji:
                                self.lista[k].zamknijKase(self.klientela)
                                self.lista[k].awariaStart(self.czasSerwisowania)
                                print(f"AWARIA KASY NR {k}, CZAS SERWISOWANIA: {self.czasSerwisowania}")
                        # obsluga klienta
                        self.lista[k].obsluzKlienta()
                        if self.lista[k].getActive(): print(self.lista[k].getIlePusta(), " KASA NR ", k, " STOI TYLE RUND PUSTA")
                        if self.lista[k].getIlePusta() == 5:
                            self.lista[k].zamknijKase(self.klientela)
                            print(f"ZAMKNIECIE KASY PO 5 MINUTACH NIEAKTYWNOSCI")
                        # generowanie wypadku
                        if self.lista[k].getActive() and self.lista[k].getObsluga():
                            self.generujWypadek(self.lista[k].obslugiwany, self.lista[k])

                        print(f"{self.lista[k].getActive()} ILOSC TRANSKACJI : {self.lista[k].getIloscTransakcji()}")
                        # sprawdza czy jest awaria, jesli jest to odejmuje minute od czas serwisu, jesli serwis
                        # zakonczony to konczy awarie
                        if self.lista[k].getAwaria():
                            print(f"{self.lista[k].getAwaria()}")
                            self.lista[k].serwis -= 1
                            print(f"{self.lista[k].serwis}")
                            if self.lista[k].serwis == 0:
                                self.lista[k].awariaStop()
                                self.lista[k].otworzKase()
        self.pokazStatystyki()

    def generujWypadek(self, klient: Klient, kasa: Kasa):
        if klient.exists:
            if klient.polak:
                print(f"KLIENT NIE POLAK")
                kasa.setstopTime(random.randint(0, 1))
        # zdarzenie losowe niezalezne od klienta - mleko sie rozlalo
        if random.randint(1, 10) == 5:
            kasa.setstopTime(random.randint(0, 2))
            print(f"WYPADEK random")

    def generujKlienta(self):
        for client in range(random.randint(0, 3)):
            # tutaj wlatuje statystyczny check:
            pomocniczyklient = Klient(self.klienciWszyscy)
            self.klienciWszyscy += 1
            if pomocniczyklient.karta == 1:
                self.klienciKarta += 1
            if pomocniczyklient.plastik == 1:
                self.klienciPlastik += 1
            if pomocniczyklient.polak != 1:
                self.klienciPolacy += 1

            self.klientela.append(pomocniczyklient)
            print(f"{self.klientela[client].czasObslugi}, CZAS OBSLUGI KLIENTA NR: {client}")

    def pokazStatystyki(self):
        print(f"Wszyscy klienci z dnia: {self.klienciWszyscy}")
        print(f"Klienci placacy karta: {self.klienciKarta}")
        print(f"Klienci plastki: {self.klienciPlastik}")
        self.klienciAplikacja = self.klienciKarta - self.klienciPlastik
        print(f"Klienci aplikacja: {self.klienciAplikacja}")
        print(f"Klienci polacy: {self.klienciPolacy}")