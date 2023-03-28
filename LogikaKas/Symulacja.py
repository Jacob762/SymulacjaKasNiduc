import random

from LogikaKas.Kasa import Kasa
from LogikaKas.Klient import Klient


class Simulation:
    lista = []
    klientela = []

    # statystyki dotyczące klientów
    # statystyki ogólne 
    klienciWszyscy=0
    klienciKarta=0
    klienciPlastik=0
    klienciAplikacja=0 # w sumie to można usunąc i na koniec odjąc od tych z kartą tych z plastikiem
    klienciPolacy =0
    #statystyki dzienne + godzinowe bedą w odpowiedniej pętli

    

    def __init__(self, iloscKas: int):
        self.start(iloscKas)
        self.simulatione(1,1)

    #Dodaje ilosc kas po czym inicjalizuje pierwszą kase:
    def start(self, iloscKas: int): 
        print("Simulation begins")
        for i in range(iloscKas):
            self.addKasa(i + 1)
        self.lista[0].active = True
        self.lista[0].wolna = True

    def addKasa(self, index: int):
        self.lista.append(Kasa(index, 8))

    def wypadek(self):
        if random.randint(1, 20) == 10:
            return -7

    def simulatione(self, dniPracy: int, godzinyPracy):
        for dzien in range(dniPracy):
            #statysyki dzienne

            for godziny in range (godzinyPracy):
                #statystyki godzinowe
                for i in range(60):
                    print(f"{i+1},  ITERACJA")
                    for client in range(random.randint(0, 3)):  # dodwanie klientow do ogolnej kolejki
                        # tutaj wlatuje statystyczny check:
                        pomocniczyklient=Klient(self.klienciWszyscy)
                        self.klienciWszyscy+=1
                        if pomocniczyklient.karta==1:
                            self.klienciKarta+=1
                        if pomocniczyklient.plastik==1:
                            self.klienciPlastik+=1
                        else:
                            self.klienciAplikacja+=1
                        if pomocniczyklient.polak==1:
                            self.klienciPolacy+=1
                        
                        self.klientela.append(pomocniczyklient)
                        print(f"{self.klientela[client].czasObslugi}, CZAS OBSLUGI KLIENTA NR: {client}")
                    print(len(self.klientela))
                    j = 0
                    while len(self.klientela) > 0 and j < len(self.lista):  # petla do dyspozycji nowych klientow
                        if self.lista[j].dodajKlienta(self.klientela.pop(0)) == -7:
                            j += 1
                    print(f"{len(self.lista[0].klienci)},  ZAPELNIENIE KASY")
                    if len(self.klientela) != 0:
                        print("Wszystkie kasy zajete")
                    for k in range(len(self.lista)):  # trzeba dodac zeby tylko aktywne kasy obslugiwaly klientow
                        self.lista[k].obsluzKlienta()
