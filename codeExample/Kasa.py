class Kasa():
    def __init__(self,stanHP: int, indeks: int, cashNaStart: float):
        self.stan_HP=stanHP
        self.indeks=indeks
        self.cash=cashNaStart

    def getCash(self):
        return self.cash
