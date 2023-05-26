import random
import time

from LogikaKas.Kasa import Kasa
from LogikaKas.Klient import Klient
from LogikaKas.myGui import MyGui
from matplotlib import pyplot as plt


class Simulation:
    lista = []
    klientela = []
    statystyki = []
    statystykiDzienne = []
    lastCall = False  # zmienna do okreslania ostatnich 20 minut w sklepie
    dziejeSie = False  # zmienna do okreslania wiekszego natloku klientow w dni robocze
    # atrybuty poczatkowe
    # zmieniłem na 300 bo 30 to trochę xD a i tak powinno być z 10_000
    # do testowania wygodniej 30 ale na release jednak jak wyżej
    # atrybuty poczatkowe:    
    maxIloscTransakcji = 30
    czasSerwisowania = 10
    licznikProblematycznosci = 0
    # statystyki dotyczące klientów
    # statystyki ogólne
    klienciWszyscy = 0
    klienciKarta = 0
    klienciPlastik = 0
    klienciPolacy = 0
    klienciKobiety = 0
    sredniWiek = 0
    klienciWroclaw = 0

    # statystyki godzinowe
    klienciWszyscyGodz = 0
    klienciKartaGodz = 0
    klienciPlastikGodz = 0
    klienciPolacyGodz = 0
    klienciKobietyGodz = 0
    sredniWiekGodz = 0
    klienciWroclawGodz = 0
    awarie = 0
    przepelnienieKas = 0
    # statystyki dzienne
    
    klienciWszyscyDzien = 0
    klienciKartaDzien = 0
    klienciPlastikDzien = 0
    klienciPolacyDzien = 0
    klienciKobietyDzien = 0
    sredniWiekDzien = 0
    klienciWroclawDzien = 0

    def __init__(self, iloscKas: int, dniPracy: int, godzinyPracy: int, awaryjnoscKasy: int, problematycznosc: int):
        self.start(iloscKas)
        self.gui = MyGui(iloscKas)
        self.maxIloscTransakcji = awaryjnoscKasy
        self.simulatione(dniPracy, godzinyPracy, problematycznosc)
        # Poniżej jeśli ustawiamy prawdopodobieństwo awarii kasy na 20 to awaria nastąpi 20% szybciej:


    # Dodaje ilosc kas po czym inicjalizuje pierwszą kase:
    def start(self, iloscKas: int):
        print("Simulation begins")
        for i in range(iloscKas):
            self.addKasa(i + 1)
        self.lista[0].active = True

    def addKasa(self, index: int):
        self.lista.append(Kasa(index, 8))

    def simulatione(self, dniPracy: int, godzinyPracy, problematycznosc: int):
        for dzien in range(dniPracy):
            self.dziejeSie = False
            self.lastCall = False
            self.klienciWszyscyDzien = 0
            self.klienciKartaDzien = 0
            self.klienciPlastikDzien = 0
            self.klienciPolacyDzien = 0
            self.klienciKobietyDzien = 0
            self.sredniWiekDzien = 0
            self.klienciWroclawDzien = 0
            self.awarie = 0
            self.przepelnienieKas = 0
            # statysyki dzienne
            print(f"DZIEN {dzien}")
            for godziny in range(godzinyPracy):
                # statystyki godzinowe
                self.klienciWszyscyGodz = 0
                self.klienciKartaGodz = 0
                self.klienciPlastikGodz = 0
                self.klienciPolacyGodz = 0
                self.klienciKobietyGodz = 0
                self.sredniWiekGodz = 0
                self.klienciWroclawGodz = 0

                if godziny + 7 == 12 or godziny + 7 == 16:  # miedzy 12 a 14 i miedzy 16 a 18 wzmozona aktywnosc ludzi
                    self.dziejeSie = True
                elif godziny + 7 == 14 or godziny + 7 == 18:
                    self.dziejeSie = False
                for i in range(60):
                    # GUI petla do sprawdzenia koloru kas
                    # time.sleep(0.2)
                    for k in range(len(self.lista)):
                        if self.lista[k].getActive():
                            self.gui.kasa_change_color(k, "green")
                        if not self.lista[k].getActive():
                            self.gui.kasa_change_color(k, "red")
                        if self.lista[k].getAwaria():
                            self.gui.kasa_change_color(k, "gray")
                        if self.lista[k].getWypadek():
                            self.gui.kasa_change_color(k, "orange")

                    print(f"{i + 1},  ITERACJA")
                    # ostatnie 20 minut przed klienci nie przychodza
                    if godzinyPracy - godziny == 1 and i == 40:
                        self.lastCall = True
                    # dodwanie klientow do ogolnej kolejki
                    if not self.lastCall:
                        self.generujKlienta(self.dziejeSie, problematycznosc)

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

                    # GUI petla do klientow przy kasie
                    for k in range(len(self.lista)):
                        self.gui.klienci_change_color(k, self.lista[k].getSize())
                    #   time.sleep(0.2)    odkomentowanie przywraca normalne dzialanie gui

                    if len(self.klientela) != 0:
                        print("Wszystkie kasy zajete")
                        self.przepelnienieKas += 1  # liczymy przepelnienie kas
                    # obsluga klienta
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
                                self.awarie += 1  # liczymy awarie
                        # obsluga klienta
                        self.lista[k].obsluzKlienta()
                        if self.lista[k].obslugiwany == self.lista[k].straznik:
                            # jesli kasa jest pusta to wtedy:
                            # sprawdza czy nie ma za duzo pieniedzy
                            if self.lista[k].ilePieniedzy >= 10_000:
                                print("Kasa przepełniona! Przepraszamy. Względy bezpieczenstwa")
                                self.lista[k].setstopTime(5)
                                self.lista[k].ilePieniedzy = 2_000

                        if self.lista[k].getActive():
                            print(self.lista[k].getIlePusta(), " KASA NR ", k, " STOI TYLE RUND PUSTA")
                        if self.lista[k].getIlePusta() == 5:
                            self.lista[k].zamknijKase(self.klientela)
                            print(f"ZAMKNIECIE KASY PO 5 MINUTACH NIEAKTYWNOSCI")
                        # generowanie wypadku
                        if self.lista[k].getActive() and self.lista[k].getObsluga():
                            self.generujWypadek(self.lista[k].obslugiwany, self.lista[k])

                        # tutaj sie konczy obsluga klienta

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

                self.zapiszStatystykiGodzinowe(dzien, godziny)
                print(self.statystyki)
            self.pokazStatystyki()
            self.zapiszStatystykiDzienne()
        # self.gui.run()
        # funkcja do wykresu, pierwszy atrybut to dni pracy a drugi to lista do osi y, jej dlugosc musi byc rowna dniom pracy

        self.narysujWykres(dniPracy, self.statystykiDzienne)

        #DO DOPRACOWANIA
        #self.narysujWykres(dniPracy, self.statystykiDzienne)
        self.gui.run()


    def generujWypadek(self, klient: Klient, kasa: Kasa):
        if klient.exists:
            if klient.polak:
                print(f"KLIENT NIE POLAK")
                kasa.setstopTime(random.randint(0, 1))
        # zdarzenie losowe niezalezne od klienta - mleko sie rozlalo
        if random.randint(1, 10) == 5:
            kasa.setstopTime(random.randint(0, 2))
            print(f"WYPADEK random")

    def zapiszStatystykiDzienne(self):
        statyDzienne = [
            self.klienciWszyscyDzien, self.klienciKobietyDzien, self.klienciWszyscyDzien - self.klienciKobietyDzien,
                                                                self.sredniWiekDzien / self.klienciWszyscyDzien,
            self.klienciKartaDzien,
                                                                self.klienciWszyscyDzien - self.klienciKartaDzien,
                                                                self.klienciWszyscyDzien - self.klienciPlastikDzien,
            self.klienciPlastikDzien, self.klienciPolacyDzien, self.klienciWszyscyDzien - self.klienciPolacyDzien,
            self.klienciWroclawDzien, self.klienciWszyscyDzien - self.klienciWroclawDzien,
            self.awarie, self.przepelnienieKas
        ]
        self.statystykiDzienne.append(statyDzienne)

    def zapiszStatystykiGodzinowe(self, dzien, godzina):
        
        # wszyscy[0],karta[1], kobiety, meżczyźni, sredniwiek,bez karty, aplikacja, plastik, polacy, niepolacy, klienci z wrocławia, klienci z nieWrocławia
        statyGodzinowe = [

            self.klienciWszyscyGodz, self.klienciKobietyGodz, self.klienciWszyscyGodz - self.klienciKobietyGodz,
                                                              self.sredniWiekGodz / self.klienciWszyscyGodz,
            self.klienciKartaGodz,
                                                              self.klienciWszyscyGodz - self.klienciKartaGodz,
                                                              self.klienciWszyscyGodz - self.klienciPlastikGodz,
            self.klienciPlastikGodz, self.klienciPolacyGodz, self.klienciWszyscyGodz - self.klienciPolacyGodz,
            self.klienciWroclawGodz, self.klienciWszyscyGodz - self.klienciWroclawGodz]
        # pomoc = [dzien + 1, godzina + 1, statyGodzinowe]
        self.statystyki.append(statyGodzinowe)
            self.awarie,self.przepelnienieKas,
        self.klienciWszyscyGodz, self.klienciKobietyGodz, self.klienciWszyscyGodz - self.klienciKobietyGodz,
        self.sredniWiekGodz / self.klienciWszyscyGodz, self.klienciKartaGodz,
        self.klienciWszyscyGodz - self.klienciKartaGodz, self.klienciWszyscyGodz - self.klienciPlastikGodz,
        self.klienciPlastikGodz, self.klienciPolacyGodz, self.klienciWszyscyGodz - self.klienciPolacyGodz,
        self.klienciWroclawGodz, self.klienciWszyscyGodz - self.klienciWroclawGodz]
        pomoc = [dzien + 1, godzina + 1, statyGodzinowe]
        self.statystyki.append(pomoc)


    def generujKlienta(self, tlum: bool, problematycznosc: int):
        if tlum:
            print(f"Tlum")
            maxLosowanie = 7  # zmienna okreslajaca maksymalna skrajna liczbe do losowania ilosci klientow
            minLosowanie = 3
        else:
            maxLosowanie = 3
            minLosowanie = 0
        for client in range(random.randint(minLosowanie, maxLosowanie)):
            # tutaj wlatuje statystyczny check:
            if self.licznikProblematycznosci == problematycznosc:
                pomocniczyklient = Klient(self.klienciWszyscy, True)
                self.licznikProblematycznosci = 0
            else:
                pomocniczyklient = Klient(self.klienciWszyscy, False)
                self.licznikProblematycznosci += 1
            self.klienciWszyscy += 1
            self.klienciWszyscyGodz += 1
            self.klienciWszyscyDzien += 1
            if pomocniczyklient.karta == 1:
                self.klienciKarta += 1
                self.klienciKartaGodz += 1
                self.klienciKartaDzien += 1
            if pomocniczyklient.plastik == 1:
                self.klienciPlastik += 1
                self.klienciPlastikGodz += 1
                self.klienciPlastikDzien += 1
            if pomocniczyklient.polak != 1:
                self.klienciPolacy += 1
                self.klienciPolacyGodz += 1
                self.klienciPolacyDzien += 1
            if pomocniczyklient.kobieta == 1:
                self.klienciKobiety += 1
                self.klienciKobietyDzien += 1
                self.klienciKobietyGodz += 1
            if pomocniczyklient.wroclaw == 1:
                self.klienciWroclaw += 1
                self.klienciWroclawDzien += 1
                self.klienciWroclawGodz += 1

            self.sredniWiek += pomocniczyklient.wiek
            self.sredniWiekDzien += pomocniczyklient.wiek
            self.sredniWiekGodz += pomocniczyklient.wiek

            self.klientela.append(pomocniczyklient)
            print(f"{self.klientela[client].czasObslugi}, CZAS OBSLUGI KLIENTA NR: {client}")

    # tutaj trzeba zmienic
    def pokazStatystyki(self):
        print(f"Wszyscy klienci: {self.klienciWszyscy}")
        print(f"Klienci placacy karta: {self.klienciKarta}")
        print(f"Klienci plastki: {self.klienciPlastik}")
        self.klienciAplikacja = self.klienciKarta - self.klienciPlastik
        print(f"Klienci aplikacja: {self.klienciAplikacja}")
        print(f"Klienci polacy: {self.klienciPolacy}")
        print(f"Ile kobiet kupiło w sklepie: {self.klienciKobiety}")
        print(f"Ile mężczyzn było w sklepie: {self.klienciWszyscy - self.klienciKobiety}")
        print(f"sredni wiek klienta: {self.sredniWiek / self.klienciWszyscy}")
        print(f"Klienci z wrocławia: {self.klienciWroclaw}")
        print(f"Klienci z poza wrocławia: {self.klienciWszyscy - self.klienciWroclaw}")
        print(f"Ilosc awarii: {self.awarie}")

    def narysujWykres(self, x, dane):
        temp = []
        warx = []
        for i in range(x):
            warx.append(i)
        fig = plt.figure("Wykres 1")
        for i in range(x):
            temp.append(dane[i][0])
        plt.plot(warx, temp)
        plt.title('Ilosc klientow w ciagu x dni')
        plt.xlabel('Dni')
        plt.ylabel('Wszyscy klienci danego dnia')
        plt.savefig(f"Wykres 1")
        fig = plt.figure("Wykres 2")
        for i in range(x):
            temp.pop()
        for i in range(x):
            temp.append(dane[i][1])  # trzeba ogarnac append
        plt.plot(warx, temp)
        plt.title('Ilosc kobiet w sklepie w ciagu x dni')
        plt.xlabel('Dni')
        plt.ylabel('Ilosc kobiet danego dnia')
        plt.savefig(f"Wykres 2")
        fig = plt.figure("Wykres 3")
        for i in range(x):
            temp.pop()
        for i in range(x):
            temp.append(dane[i][2])
        plt.plot(warx, temp)
        plt.title('Ilosc mezczyzn w ciagu x dni')
        plt.xlabel('Dni')
        plt.ylabel('Ilosc  mezczyzn danego dnia')
        plt.savefig(f"Wykres 3")
        fig = plt.figure("Wykres 4")
        for i in range(x):
            temp.pop()
        for i in range(x):
            temp.append(dane[i][3])
        plt.plot(warx, temp)
        plt.title('Sredni wiek w przeciagu x dni')
        plt.xlabel('Dni')
        plt.ylabel('Sredni wiek danego dnia danego dnia')
        plt.savefig(f"Wykres 4")
        fig = plt.figure("Wykres 5")
        for i in range(x):
            temp.pop()
        for i in range(x):
            temp.append(dane[i][4])
        plt.plot(warx, temp)
        plt.title('Ilosc klientow placacych karta w ciagu x dni')
        plt.xlabel('Dni')
        plt.ylabel('Platnosci gotowka danego dnia')
        plt.savefig(f"Wykres 5")
        fig = plt.figure("Wykres 6")
        for i in range(x):
            temp.pop()
        for i in range(x):
            temp.append(dane[i][5])
        plt.plot(warx, temp)
        plt.title('Ilosc klientow placacych gotowka w ciagu x dni')
        plt.xlabel('Dni')
        plt.ylabel('Platnosci telefonem danego dnia')
        plt.savefig(f"Wykres 6")
        fig = plt.figure("Wykres 7")
        for i in range(x):
            temp.pop()
        for i in range(x):
            temp.append(dane[i][6])
        plt.plot(warx, temp)
        plt.title('Ilosc klientow placacych telefonem w ciagu x dni')
        plt.xlabel('Dni')
        plt.ylabel('Platnosci fizyczna karta danego dnia')
        plt.savefig(f"Wykres 7")
        fig = plt.figure("Wykres 8")
        for i in range(x):
            temp.pop()
        for i in range(x):
            temp.append(dane[i][7])
        plt.plot(warx, temp)
        plt.title('Ilosc klientow placacych plastkiowa karta w ciagu x dni')
        plt.xlabel('Dni')
        plt.ylabel('Wszyscy polacy danego dnia')
        plt.savefig(f"Wykres 8")
        fig = plt.figure("Wykres 9")
        for i in range(x):
            temp.pop()
        for i in range(x):
            temp.append(dane[i][8])
        plt.plot(warx, temp)
        plt.title('Ilosc polakow w ciagu x dni')
        plt.xlabel('Dni')
        plt.ylabel('Wszyscy obcokrajowcy danego dnia')
        plt.savefig(f"Wykres 9")
        fig = plt.figure("Wykres 10")
        for i in range(x):
            temp.pop()
        for i in range(x):
            temp.append(dane[i][9])
        plt.plot(warx, temp)
        plt.title('Ilosc obcokrajowcow w ciagu x dni')
        plt.xlabel('Dni')
        plt.ylabel('Wszyscy klienci z Wroclawia danego dnia')
        plt.savefig(f"Wykres 10")
        fig = plt.figure("Wykres 11")
        for i in range(x):
            temp.pop()
        for i in range(x):
            temp.append(dane[i][10])
        plt.plot(warx, temp)
        plt.title('Ilosc klientow z Wroclawia w ciagu x dni')
        plt.xlabel('Dni')
        plt.ylabel('Wszyscy klienci spoza Wroclawia danego dnia')
        plt.savefig(f"Wykres 11")
        fig = plt.figure("Wykres 12")
        for i in range(x):
            temp.pop()
        for i in range(x):
            temp.append(dane[i][11])
        plt.plot(warx, temp)
        plt.title('Ilosc klientu spoza Wroclawia w ciagu x dni')
        plt.xlabel('Dni')
        plt.ylabel('Wszyscy klienci danego dnia')
        plt.savefig(f"Wykres 12")
        fig = plt.figure("Wykres 13")
        for i in range(x):
            temp.pop()
        for i in range(x):
            temp.append(dane[i][12])
        plt.plot(warx, temp)
        plt.title('Ilosc awarii w ciagu x dni')
        plt.xlabel('Dni')
        plt.ylabel('Wszystkie awarie danego dnia')
        plt.savefig(f"Wykres 13")
        fig = plt.figure("Wykres 14")
        for i in range(x):
            temp.pop()
        for i in range(x):
            temp.append(dane[i][13])
        plt.plot(warx, temp)
        plt.title('Ilosc przepelnienia kas w ciagu x dni')
        plt.xlabel('Dni')
        plt.ylabel('Przepelnienia kas danego dnia')
        plt.savefig(f"Wykres 14")
