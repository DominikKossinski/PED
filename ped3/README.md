# Ocena ważności atrybutów

## Brakujące kategorie

Skrypt *download_categories.py* pozwala na pobranie danych, które zawierają
brakujące kategorie w oryginalnym zbiorze danych.

Do uruchomienia skryptu potrzebny jest wygenerowany
wcześniej klucz (ang. API key), który będzie przechowywany
w zmiennej środowiskowej o nazwie *API_KEY*.

```commandline
python download_categories.py
    -h, --help                      show this help message and exit
    --grouped-path GROUPED_PATH     Path to grouped data set
    --path PATH                     Path to save directory (default '../categories_data')

```
