# Projekt Eksploracja danych - YouTube trending videos

### Pliki z rozwiązaniami poszczególnych etapów:

- ETAP 1 - **PED_1.ipynb**
- ETAP 2 - **PED_2.ipynb**

### Instrukcje uruchomiania poszczególnych skryptów

Skrypt do uzupełniania brakujących id wyznacza on id na podstawie linku do obrazka filmu. Uruchomienie:

```commandline
python preprocess_ids.py
```

Skrypt do grupowania danych po id (wymaga wcześniejszego uruchomienia skryptu do uzupełniania id). Grupuje dane po
wygenerowanym atrybucie **new_video_id**, który jest kopią atrybutu
**video_id** albo jest pozyskiwany z **thumbnail_link**.

```commandline
python group_data.py
```

Skrypt do pobierania obrazków filmów (wymaga wcześniejszego uruchomienia skrypty do grupowania) pobiera unikalne obrazy
ze zbioru filmów i zapisuje je w folderze **images**. Pozwala na pobranie obrazów w trzech rozmiarach.

```commandline
python images_downloading.py
    -h, --help                                  show this help message and exit
    --size {default,hqdefault,maxresdefault}    Image size
```

Skrypt do czytania tekstu na obrazach.

```commandline
python ocr_processing.py
    -h, --help                                  show this help message and exit
    --size {default,hqdefault,maxresdefault}    Image size
```

Skrypt do sprawdzania emocji na obrazach.

```commandline
python extract_emotions.py
    -h, --help                                  show this help message and exit
    --size {default,hqdefault,maxresdefault}    Image size
```



