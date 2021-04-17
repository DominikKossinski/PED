# Ocena ważności atrybutów

## Brakujące kategorie

Skrypt *download_categories.py* pozwala na pobranie danych, które zawierają brakujące kategorie w oryginalnym zbiorze
danych.

Do uruchomienia skryptu potrzebny jest wygenerowany wcześniej klucz (ang. API key), który będzie przechowywany w
zmiennej środowiskowej o nazwie *API_KEY*.

```commandline
python download_categories.py
    -h, --help                      show this help message and exit
    --grouped-path GROUPED_PATH     Path to grouped data set
    --path PATH                     Path to save directory (default '../categories_data')

```

Skrypt *group_tokenized_data_by_id.py* grupuje dane tekstowe uzyskane w pierwszym etapie, które zostały poddane
tokenizacji. Dane grupowane są wg wygenerowanego identyfikatora z linka do url.

```commandline
python group_tokenized_data_by_id.py

```

Skrypt *prepare_old_categories* służy do przygotowania kategorii z oryginalnego zbioru danych po zgrupowaniu. Jego
zadaniem jest znalezienie jednoznacznej kategorii, do której należy film, usuwa wartości *nan* o ile jest to możliwe.

```commandline
python prepare_old_categories.py
```
