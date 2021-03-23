# Projekt Eksploracja danych - YouTube trending videos

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

Skrypt do pobierania obrazków filmów (wymaga wcześniejszego uruchomienia skrypty do grupowania) pobiera unikalne
obrazy ze zbioru filmów i zapisuje je w folderze **images**. Pozwala na pobranie obrazów
w trzech rozmiarach.
```commandline
python images_downloading.py
    -h, --help                                  show this help message and exit
    --size {default,hqdefault,maxresdefault}    Image size
```


