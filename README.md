# Dobra chłopaki sprawa jest taka że siedze w lobby hotelowym i git mi się wypierdala!!! ZARAZ MNIE COŚ PIERDOLNIE
#KUBA KLAWON SORRY ŻE TAK CHUJOWO ALE INACZEJ PLIKÓW NIE BYŁEM W STANIE DODAĆ. MAM NADZIEJE ŻE NADAL MIĘDZY NAMI SZTAMA KOCIE


# SymulacjaKasNiduc

## TO DO:

1. Klasa 'Kasa'  
    - status aktywna/zamknieta  
    - zuzycie kasy (totalna ilosc transakcji)
    - wolna / zajeta
    - kolor  
    - naprawa trwa 3h  
1. Klasa klient:  
    - ~~KOlor~~  
    - nr kasy (??) imo niepotrzebne   
    - ~~ilosc minut obsługi (int)~~  
    
    --------
    - ~~polak/ mowi po polsku~~
    - ~~karta biedronki/aplikacja~~
    - ~~rodzina~~  
    - ~~karta/ gotówka~~  
    - ~~nr transakcji a.k.a id klienta ale z klientem trudniej bedzie~~   
1. Klasa Kolejka:  
    - przypisana do kasy
    - znajdują się w niej klienci
    - ma maksymalną pojemnośc 
    - ma aktualną pojemnosc  
    - wysyła info do symulacji jeśli za dużo ludzi  
    - mało ludzi -> 1 kolejka, dużo-> więcej 
1. Klasa Symulacja/logika:  
    - zajmuje sie tym burdelem  
    - przekazuje info z logiką do gui (kolory prostokątów)
    - iteracja trwa 1 minutę  
    - generuje wypadki:  
        - za duża kolejka  
        - za dużo transkacji
        - nie ma wydać/problemy z płatnością  
        - nie ma naklejki  
        - za duzo pieniedzy w kasie (kwestia bezpieczeństwa)  
        - pani nie ma jak wydac  
        - mleko się rozlało- kase trzeba posprzątać  
        - obcokrajowiec nie mówi po polsku  

1. GUI:  
    - Kasy:  
        - zielona- aktywna
        - czerwona- zamknieta
        - pomarańczowa- klient debil robi problemy (?)
        - magenta- kasa w naprawie(?)
    - Klient w kolejce:  
        - jest- czarny
        - nie ma- brak/biały 
1. zapisywanie danych:  
    - okres ok 6 miesiecy?  
    - dane typu:
        - srednia liczba klientów na dziennie/godzinowo/ w zalezności od dnia??
        - czym płacą (karta/gotówka)  
        - karta lojalnościowa ?  
        - czy mają rodzine i jak tak to ile osob  
        - cena zakupów x ilość członków rodziny  
        - czy karte lojalnościowa w telefonie czy plastik  
1. zrobienie wykresów


