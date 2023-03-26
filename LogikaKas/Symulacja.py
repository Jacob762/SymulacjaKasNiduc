import random

from LogikaKas.Kasa import Kasa
from LogikaKas.Klient import Klient


class Simulation:
    lista = []  # lista kas
    klientela = []  # kolejka ogolna

    def __init__(self, iloscKas: int):
        self.start(iloscKas)
        self.simulatione(50)

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
        temp = False
        for i in range(czasPracy):
            print(i, " ITERACJA")
            if czasPracy - i >= 15:
                for client in range(random.randint(0, 2)):  # dodwanie klientow do ogolnej kolejki
                    self.klientela.append(Klient())
                    print(self.klientela[client].czasObslugi, " CZAS OBSLUGI KLIENTA NR ", client)
                print(len(self.klientela))
            j = 0
            while len(self.klientela) > 0 and j < len(self.lista):  # petla do dyspozycji nowych klientow
                if not self.lista[j].getActive() and self.lista[j]: self.lista[j].otworzKase()
                if self.lista[j].dodajKlienta(self.klientela.pop(0)) == -7: # zrobic zeby jesli >1 kasa otwarta to zeby klient mogl wybierac, tez trzeba dobrac warunki zeby
                    j += 1                                                  # nie trzymac x otwartych kas dla malej ilosci klientow
            for client in range(len(self.lista)):
                if self.lista[client].getActive():
                    print(len(self.lista[client].klienci), " ZAPELNIENIE KASY NR ", client + 1)
            if len(self.klientela) != 0:
                print("Wszystkie kasy zajete")
            for k in range(len(self.lista)):  # trzeba dodac zeby tylko aktywne kasy obslugiwaly klientow
                if self.lista[k].obsluzKlienta() == -7:
                    break
                print(self.lista[k].getIlePusta(), " KASA NR ", k, " STOI TYLE RUND PUSTA")
                if self.lista[k].getIlePusta() == 5:
                    self.lista[k].zamknijKase()

        for k in range(len(self.lista)):
            if self.lista[k].getActive(): print(len(self.lista[k].klienci), " TYLE KLIENTOW ZOSTALO W KASIE NR ", k)
            temp = True
            if len(self.lista[k].klienci)==0:
                self.lista[k].zamknijKase()
        print(len(self.klientela), " TYLE CZEKA NA OBSLUGE")
        o = 0
        while len(self.klientela) > 0 or temp:
            print(o, " ITERACJA NADGODZINOWA")
            for client in range(len(self.lista)):
                if self.lista[client].getActive():
                    print(len(self.lista[client].klienci), " ZAPELNIENIE KASY NR ", client + 1)
            if len(self.klientela) != 0:
                print("Wszystkie kasy zajete")
            for k in range(len(self.lista)):  # trzeba dodac zeby tylko aktywne kasy obslugiwaly klientow
                if self.lista[k].obsluzKlienta() == -7:
                    break
                print(self.lista[k].getIlePusta(), " KASA NR ", k, " STOI TYLE RUND PUSTA")
                if self.lista[k].getIlePusta() == 1:
                    self.lista[k].zamknijKase()
                    temp = False
            o+=1


