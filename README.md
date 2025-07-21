#  Item Printer – Aplikacja do drukowania etykiet na drukarce Zebra

##  Opis projektu
Item Printer to prosta aplikacja w **Python + PyQt5**, służąca do drukowania etykiet na drukarkach **Zebra**.  
Pozwala użytkownikowi wprowadzić listę pozycji (**Item**) wraz z ilością (**Qty**), a następnie przesłać dane w formacie **ZPL** bezpośrednio do drukarki przez sieć.

---

## 🖼 Wygląd aplikacji
- Tabela z dwoma kolumnami:
  - **Item** – kod produktu (maks. 12 cyfr)
  - **Qty** – ilość etykiet do wydrukowania (1–99)
- Przyciski:
  - **Dodaj wiersz** – dodaje nową pozycję
  - **Usuń zaznaczony** – usuwa zaznaczony wiersz
  - **Usuń wszystkie** – czyści tabelę
  - **Drukuj** – wysyła dane do drukarki

---

##  Jak działa program
1. Użytkownik wprowadza dane w tabeli:
   - Kolumna `Item`: numer produktu (cyfry, max 12 znaków)
   - Kolumna `Qty`: ilość etykiet (1–99)
2. Tworzenie nowego wiersza:
   - Po przez użycie przycisku `Dodaj wiersz`
   - Po przez użycie klawisza `Enter` w kolumnie `Qty` (alternatywnie)
3. Usuwanie wiersza:
   - Po przez użycie przycisku `Usuń zaznaczony` (pojedyńczy wiersz lub zaznaczone wiersze)
   - Po przez użycie przycisku `Usuń wszystkie`
4. Dynamiczna wielkość okna programu:
   - Okienko automatycznie rozszerza się do ilości 10 wierszy.
   - Po przekroczeniu 10 wierszy z boku okienka pojawia się pasek nawigacyjny (alternatywnie skroll)
5. Kliknięcie **Drukuj**:
   - Program waliduje dane (sprawdza poprawność kodu i ilości)
   - Generuje komendy **ZPL** w oparciu o konfigurację (IP drukarki, port, rozmiar czcionki)
   - Wysyła dane do drukarki przez **TCP/IP**
6. Wyświetlany jest komunikat o powodzeniu lub błędzie.

---

##  Struktura projektu
project/    
│   
├── main.py # Główna aplikacja (GUI)    
├── config.json # Plik konfiguracyjny   
├── config_loader.py # Klasa Config do wczytywania ustawień     
├── printer/    
│ └── zebra_printer.py # Klasa ZebraPrinter (wysyłanie ZPL)     
├── utils/  
│ └── validators.py # Walidacja pól Item i Qty  
└── dist/ # Folder po kompilacji (PyInstaller)


## Konfiguracja (plik `config.json`)
Przed uruchomieniem programu należy skonfigurować plik `config.json`:

```json
{
    "printer_ip": "192.168.0.100",
    "printer_port": 9100,           
    "font_size": 16                 
}
```

- printer_ip – adres IP drukarki Zebra
- printer_port – port TCP drukarki (domyślnie 9100)
- font_size – rozmiar czcionki na etykiecie

## Uruchamianie aplikacji
W trybie deweloperskim:
- Zainstaluj wymagane biblioteki:
  - (bash) pip install pyqt5 pyinstaller
- Uruchom aplikację:
  - python main.py


## Kompilacja do EXE (Windows)
- Do stworzenia pliku wykonywalnego używamy PyInstaller:
  - (bash) pyinstaller --onefile --noconsole main.py
- Po kompilacji plik main.exe znajdzie się w katalogu dist/.
  - (bash) .\dist\main.exe


##  Walidacja danych
- Item: tylko cyfry, maks. 12 znaków

- Qty: liczba całkowita 1–99

Jeśli dane są błędne, program wyświetli komunikat i przerwie drukowanie.

## Drukowanie
- Wysyłanie etykiet do drukarki odbywa się przez TCP/IP (socket)

- Format etykiety to Zebra Programming Language (ZPL):
```
^XA
^C128
^CF0,{font_size}
^FO50,30^FD<Item>^FS
^CF0,30
^FO50,80^FD<DATA>^FS
^XZ
```

## Najczęstsze problemy
- Błąd "Failed to start embedded python interpreter!"
  - Zamknij wszystkie instancje EXE, usuń dist/ i build/, skompiluj ponownie jako administrator.

- Brak połączenia z drukarką
  - Sprawdź printer_ip, printer_port i czy drukarka odpowiada na ping.

- Antywirus blokuje EXE
  - Dodaj wyjątek w antywirusie lub uruchom jako administrator.