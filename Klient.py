import random


class Klient:


    def __init__(self,idTransakcji: int):
        # false=0 i chyba cała reszta, true=1
        kolor = "black"
        self.exists = True
        self.czasObslugi = random.randint(1, 2)
        self.polak=random.randint(0, 5)
        self.idTransakcji=idTransakcji
        self.rodzina = random.randint(0,5)
        self.wydatek = random.randint(10, 400)*self.rodzina #  w pln
        self.karta = random.randint(0,1)
        if self.karta==1:
            self.plastik=random.randint(0, 2)# co 3 osoba plastik
        else :
            self.plastik=0
        self.kobieta=random.randint(0, 2)
        self.wiek= random.randint(10, 93)
        #skad jest -> wrocław czy okolice :))
        self.wroclaw=random.randint(0, 2) #zakladam że to większy sklep na obrzeżach typu bielany wrocławskie



