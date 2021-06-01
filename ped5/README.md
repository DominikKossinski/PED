## Zbieranie danych nie-trending

Skrypt *download_videos_data.py* służy do pobrania filmów, które nie były filmami trending. Dodatkowo filtruje on filmy
tak, aby uzyskać zbiór filmów z kategorii, które występują tylko w oryginalnym zbiorze danych.

Skrypt *download_videos_stats.py* pozwala na uzupełnienie brakujących statystyk opisujących dane, a nie zwracanych w
żądaniu /search.

Plik *mock_body.json* pozwalał na testowanie, skryptu parsującego dane do pliku csv bez konieczności wysyłania
rzeczywistych żądań do serwera YouTube Api.

Skrypt *add_numeric_attrs.py* uzupełnia brakujące atrybuty numeryczne, które były
wyznaczane na podstawie innych atrybutów.

Skrypt *extract_domains.py* zbiera dane na temat linków zamieszczonych w opisach.

Skrypt *refresh_trending_data.py* pobiera odświeżone dane trending.

Skrypt *tfidf.py* zawiera funkcję do dodawania atrybutów tf-idf.

Skrypt *tokenize_data.py* tokenizuje dane tekstowe.

Skrypt *tokenize_tags* przetwarza tagi zamieszczone przy filmach.
