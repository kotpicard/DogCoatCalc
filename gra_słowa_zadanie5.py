import random

def gra_przedluzanie_slow():
    slownik = "słowa_na_D.txt"
    print("Witaj w grze 'Przedłużanie słów'!")
    print("Zaczynamy od pustego ciągu znaków. Na zmianę dodajemy po jednej literze.")
    print("Grę przegrywa osoba, która nie będzie mogła przedłużyć słowa.")
    print("Aby zakończyć grę, wpisz 'koniec'.")
    print("-" * 40)

    def wczytaj_slownik():
        # slownik = input("Podaj plik słownikowy ")
        with open(slownik) as f:
            return set(line.strip().lower() for line in f if line.strip())

    def czy_mozna_przedluzyc(ciag, slownik):
        return any(ciag in slowo for slowo in slownik)


    def ruch_uzytkownik(slownik):
         while True:
            wybor = input("Dodaj literę lub wpisz 'koniec': ").strip().lower()
            if wybor == 'koniec':
                print("Gra zakończona.")
                return None

            gdzie = input("Dodaj na (p)oczątek czy (k)oniec? ").strip().lower()
            if gdzie == 'p':
                nowy_ciag = wybor + ciag
            elif gdzie == 'k':
                nowy_ciag = ciag + wybor
            else:
                print("Niepoprawny wybór, spróbuj jeszcze raz.")
                continue
            

    def uzytkownik_czy_dobrze(nowy_ciag, slownik):
          if len(litera) != 1 or not litera.isalpha():
             return("Proszę podać jedną literę.")
          #else:
               #continue

    def ruch_komputer(ciag, slownik):
        mozliwe_slowa = list(filter(lambda slowo: slowo.startswith(ciag), slownik))
        if not mozliwe_slowa:
            print("Nie można przedłużyć!Konputer wygrał!!!")
            return None

        ciag += random.choice(mozliwe_litery)
    print(f"Komputer dodał literę: '{ciag[-1]}'")
    return ciag


     # Główna logika gry
    slownik = wczytaj_slownik()
    ciag = ""

    while True:
        print(f"\nAktualny ciąg: '{ciag}'")
        # Ruch użytkownika
        ciag = ruch_uzytkownika(ciag, slownik)
        if ciag is None:
            break

        # Ruch komputera
        ciag = ruch_komputera(ciag, slownik)
        if ciag is None:
            print("Komputer nie może przedłużyć. Wygrywasz!")
            break
            
            

                


        
