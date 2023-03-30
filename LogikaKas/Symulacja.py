import random

from LogikaKas.Kasa import Kasa
from LogikaKas.Klient import Klient


class Simulation:
    lista = []
    klientela = []
    lastCall = False # zmienna do okreslania ostatnich 20 minut w sklepie
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
        self.simulatione(1, 2)

    # Dodaje ilosc kas po czym inicjalizuje pierwszą kase:
    def start(self, iloscKas: int):
        print("Simulation begins")
        for i in range(iloscKas):
            self.addKasa(i + 1)
        self.lista[0].active = True
        self.lista[0].wolna = True

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
                    if godzinyPracy - godziny == 1 and i == 40: #ostatnie 20 minut przed klienci nie przychodza
                        self.lastCall = True
                    if not self.lastCall:
                        for client in range(random.randint(0, 3)):  # dodwanie klientow do ogolnej kolejki
                            # tutaj wlatuje statystyczny check:
                            pomocniczyklient = Klient(self.klienciWszyscy)
                            self.klienciWszyscy += 1
                            if pomocniczyklient.karta == 1:
                                self.klienciKarta += 1
                            if pomocniczyklient.plastik == 1:
                                self.klienciPlastik += 1
                            else:
                                self.klienciAplikacja += 1
                            if pomocniczyklient.polak == 1:
                                self.klienciPolacy += 1

                            self.klientela.append(pomocniczyklient)
                            print(f"{self.klientela[client].czasObslugi}, CZAS OBSLUGI KLIENTA NR: {client}")
                    print(len(self.klientela))
                    j = 0
                    while len(self.klientela) > 0 and j < len(self.lista):  # petla do dyspozycji nowych klientow
                        if self.lista[j].dodajKlienta(self.klientela.pop(0)) == -7:
                            j += 1
                    for k in range(len(self.lista)):
                        print(f"{len(self.lista[k].klienci)},  ZAPELNIENIE KASY")
                        if self.lista[k].getstopTime() == 0 and self.lista[k].getWypadek():
                            self.lista[k].resetstopTime()
                        elif self.lista[k].getstopTime() != 0:
                            self.lista[k].stopTime -= 1
                        print(f"CZAS OCZEKIWANIA NA KONIEC WYPADKU: {self.lista[k].stopTime}")
                    if len(self.klientela) != 0:
                        print("Wszystkie kasy zajete")
                    for k in range(len(self.lista)):# trzeba dodac zeby tylko aktywne kasy obslugiwaly klientow
                        self.lista[k].obsluzKlienta()
                        if self.lista[k].getActive():
                            self.generujWypadek(self.lista[k].obslugiwany, self.lista[k])
                        print(f"{self.lista[k].getActive()} ILOSC TRANSKACJI : {self.lista[k].getIloscTransakcji()}")
                        if self.lista[k].getIloscTransakcji() == self.maxIloscTransakcji: # sprawdza czy kasa osiagnela maksymalna ilosc transkacji
                            self.lista[k].zamknijKase(self.klientela)
                            self.lista[k].awariaStart(self.czasSerwisowania)
                            print(f"AWARIA KASY NR {k}, CZAS SERWISOWANIA: {self.czasSerwisowania}")

                    for k in range(len(self.lista)): # sprawdza czy jest awaria, jesli jest to odejmuje minute od czas serwisu,
                        if self.lista[k].getAwaria(): # jesli serwis zakonczony to konczy awarie
                            print(f"{self.lista[k].getAwaria()}")
                            self.lista[k].serwis -= 1
                            print(f"{self.lista[k].serwis}")
                            if self.lista[k].serwis == 0:
                                self.lista[k].awariaStop()
                                self.lista[k].otworzKase()


    def generujWypadek(self, klient : Klient, kasa : Kasa):
        #if klient:
           # if klient.polak == 0:
              #  print("WYPADEK POLAK")
               # kasa.setstopTime(random.randint(0,1))
        if random.randint(10, 10) == 10: # zdarzenie losowe niezalezne od klienta - mleko sie rozlalo
            kasa.setstopTime(random.randint(0,2))
            print("WYPADEK random")
