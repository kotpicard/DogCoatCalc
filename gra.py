def intro():
    return "Witaj w grze 'Przedłużanie słów'!\nZaczynamy od pustego ciągu znaków. Na zmianę dodajemy po jednej literze.\nGrę przegrywa osoba, która nie będzie mogła przedłużyć słowa.\nAby zakończyć grę, wpisz 'koniec'."


def slownik(sciezka):
    with open(sciezka, encoding="utf-8") as fh:
        return [x.strip().lower() for x in fh.readlines()]


def czy_mozna_przedluzyc(ciag, slownik):
    return any(ciag in slowo and not ciag == slowo for slowo in slownik)


def wybierz_przod_tyl(obecny):
    return input_plus_minus(
        "Stan po ruchu komputera: {}. Wpisz + jeżeli chcesz dodać znak z tyłu, - jeżeli z przodu ".format(
            obecny), "") == "+" if obecny else True


def dodaj_uzytkownik_wybor(obecny):
    return test_koniec(input_litery, "Dopisz literę do " + obecny + ":",
                       input("Dopisz literę do " + obecny + ":")) if obecny else test_koniec(input_litery,
                                                                                             "Podaj pierwszą literę: ",
                                                                                             input(
                                                                                                 intro() + "Podaj pierwszą literę: "))


def input_litery(prompt, test):
    return test if test in [x for x in "abcdefghijklmnopqrstuwvxyząćęłńóśźż"] else input_litery(prompt, input(prompt))


def input_plus_minus(prompt, test):
    return test if test in ["+", "-"] else input_plus_minus(prompt, input(prompt))


def dodaj_uzytkownik(obecny):
    return obecny + dodaj_uzytkownik_wybor(obecny) if wybierz_przod_tyl(obecny) else dodaj_uzytkownik_wybor(
        obecny) + obecny


def test_koniec(fun, prompt, test):
    return komunikat_koniec() if test == "koniec" else fun(prompt, test)


def komunikat_koniec():
    return "!koniec"


def komunikat_przegrana(kto, obecny):
    return "!Przegrana. Nie możesz przedłużyć słowa " + obecny if kto else "!Wygrana. Komputer nie może przedłużyć słowa " + obecny


def komunikat_przegrana_2(obecny):
    return "!Przegrana. W słowniku nie ma słowa, które zawiera ciąg " + obecny


def ruch_uzytkownik(obecny, slownik):
    return komunikat_przegrana(True, obecny) if not czy_mozna_przedluzyc(obecny, slownik) else dodaj_uzytkownik(obecny)


def wybierz_mozliwosc(obecny, slownik):
    return [x for x in slownik if obecny in x][0]


def dodaj_komputer_tyl(indeks, mozliwosc, dlugosc):
    return mozliwosc[indeks:indeks + dlugosc + 1]


def dodaj_komputer_przod(indeks, mozliwosc, dlugosc):
    return mozliwosc[indeks - 1:indeks + dlugosc]


def ind(mozliwosc, obecny):
    return mozliwosc.find(obecny)


def dodaj_komputer(obecny, slownik):
    return dodaj_komputer_tyl(ind(wybierz_mozliwosc(obecny, slownik), obecny), wybierz_mozliwosc(obecny, slownik),
                              len(obecny)) if ind(wybierz_mozliwosc(obecny, slownik), obecny) + len(obecny) < len(
        wybierz_mozliwosc(obecny, slownik)) else dodaj_komputer_przod(ind(wybierz_mozliwosc(obecny, slownik), obecny),
                                                                      wybierz_mozliwosc(obecny, slownik), len(obecny))


def jest_w_slowniku(obecny, slownik):
    return any([obecny in slowo for slowo in slownik])


def ruch_komputer(obecny, slownik):
    return komunikat_koniec() if "!koniec" in obecny else ((dodaj_komputer(obecny, slownik) if czy_mozna_przedluzyc(obecny, slownik) else komunikat_przegrana(False,
                                                                                                               obecny)) if jest_w_slowniku(
        obecny, slownik) else komunikat_przegrana_2(obecny))


def ruch(kto, obecny, slownik):
    return ruch_uzytkownik(obecny, slownik) if kto else ruch_komputer(obecny, slownik)


def ruch_wrapper(kto, obecny, slownik):
    return ruch_wrapper(tura(kto), ruch(tura(kto), obecny, slownik), slownik) if status(obecny) else obecny


def tura(kto):
    return 0 if kto else 1


def status(obecny):
    return True if not obecny or obecny[0] != "!" else False


def gra(sciezka):
    return ruch_wrapper(1, "", slownik(sciezka)) if not None else ""


print(gra("słowa_na_D.txt"))
