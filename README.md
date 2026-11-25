# Silnik wspomagający wybór trasy rowerowej

Silnik wnioskujący w przód i wstecz na bazie wiedzy w formacie JSON

## Struktura

- se/silnik.py: silnik wnioskujący (TODO 1–4)
- se/test_silnik.py: autotest silnika na bazie `kawa.json`
- se/test_trasa.py: testy własnej bazy (7 przypadków)
- se/sprawdz_format.py: sprawdzenie formatu bazy
- wiedza/trasa.json: baza wiedzy (21 reguł, 3 poziomy atrybutów)

## Konsultacja w trybie wstecz

=== Wnioskowanie wstecz === 

Jaka jest pogoda? (słoneczna/pochmurna/deszczowa) słoneczna  

Jaka jest prędkość wiatru (km/h)? 10 

Jakie jest Twoje zmęczenie? (brak/niewielkie/średnie/duże) duże 

Polecam: brak trasy 

Reguły: P1 -> R7 

## Dlaczego te pytania

Celem jest "decyzja", a każda reguła R zaczyna się od warunku "warunki_na_trasie", więc silnik najpierw ustala ten wniosek pośredni. Reguła P1 wymaga słonecznej pogody i wiatru poniżej 30km/h, stąd pytanie o pogodę i wiatr. Dla dobrych warunków reguły R1-R7 sprawdzają zmęczenie. Odpowiedź "duże" spełnia regułe R7, która nie ma warunku na ochotę - silnik o nią nie pyta.

## Kolejność reguł 

Gdy pasują dwie reguły, wygrywa ta, która stoi wyżej w pliku. Dlatego wyjątek P6 (pochmurno i wiatr < 10km/h) stoi przed P3.