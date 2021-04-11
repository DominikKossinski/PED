# Przetwarzanie obrazów

## Uzupełnianie *video_id*

Skrypt do uzupełniania brakujących id wyznacza on id na podstawie linku do obrazka filmu. Uruchomienie:

```commandline
python preprocess_ids.py
```

## Grupowanie obrazów

Skrypt do grupowania danych po id (wymaga wcześniejszego uruchomienia skryptu do uzupełniania id). Grupuje dane po
wygenerowanym atrybucie **new_video_id**, który jest kopią atrybutu
**video_id** albo jest pozyskiwany z **thumbnail_link**.

```commandline
python group_data.py
```

## Pobieranie obrazów

Skrypt do pobierania obrazków filmów (wymaga wcześniejszego uruchomienia skrypty do grupowania) pobiera unikalne obrazy
ze zbioru filmów i zapisuje je w folderze **images**. Pozwala na pobranie obrazów w trzech rozmiarach.

```commandline
python images_downloading.py
    -h, --help                                  show this help message and exit
    --size {default,hqdefault,maxresdefault}    Image size
```

## Emocje na obrazach

Skrypt do sprawdzania emocji na obrazach.

```commandline
python extract_emotions.py
    -h, --help                                  show this help message and exit
    --size {default,hqdefault,maxresdefault}    Image size
```

## Przetwarzanie OCR

Skrypt *extract_texts.py* pozwala na oczytanie tekstów z obrazów.

Wymaga wcześniejszego uruchomienia skryptu do pobrania obrazów znajdującego się w TODO.

```commandline
python extract_texts.py
    -h, --help                                  show this help message and exit
    --size {default,hqdefault,maxresdefault}    Image size
    --pytesseract-path PYTESSERACT_PATH         Path to pytesseract
```

## Kolory na obrazach

Skrypt **extract_colors.py** pozwala na wyodrębnienie kolorów, które często występują na zdjęciach.

```commandline
python extract_colors.py
```

## Klasyfikacja obrazów

Podjęto próbę klasyfikacji obrazów jednak nie przyniosła ona ciekawych efektów.

