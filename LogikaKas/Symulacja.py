import random

from LogikaKas.Kasa import Kasa
from LogikaKas.Klient import Klient


class Simulation:
    lista = []
    klientela = []

    def __init__(self, iloscKas: int):
        self.start(iloscKas)
        self.simulatione(15)

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

    def simulatione(self, czasPracy: int):
        for i in range(czasPracy):
            print(f"{i},  ITERACJA")
            for client in range(random.randint(0, 3)):  # dodwanie klientow do ogolnej kolejki
                self.klientela.append(Klient())
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
