# Silnik wspomagający wybór trasy rowerowej

Silnik wnioskujący w przód i wstecz na bazie wiedzy w formacie JSON

## Struktura

- `app.py`: interfejs Streamlit
- `se/silnik.py`: silnik wnioskujący
- `se/test_silnik.py`: autotest silnika na bazie `kawa.json`
- `se/test_trasa.py`: testy własnej bazy (7 przypadków)
- `se/sprawdz_format.py`: sprawdzenie formatu bazy
- `se/weryfikacja.py`: weryfikator bazy
- `wiedza/trasa.json`: baza wiedzy (21 reguł, 3 poziomy atrybutów)
- `wiedza/kawa.json`: przykładowa baza wiedzy
- `wiedza/kawa_z_bledami.json`: baza do testów weryfikatora

## Uruchomienie

python se/test_trasa.py - test mojej bazy

python se/weryfikacja.py wiedza/trasa.json - weryfikacja podanej bazy

python -m streamlit run app.py - uruchamia interfejs w aplikacji Streamlit

## Konsultacja w trybie wstecz

=== Wnioskowanie wstecz === 

Jaka jest pogoda? (słoneczna/pochmurna/deszczowa) (? = dlaczego pytam) pochmurna 

Jaka jest prędkość wiatru (km/h)? (? = dlaczego pytam) ? 

Pytam, bo sprawdzam regułę: P6: JEŚLI pogoda == 'pochmurna' ORAZ predkosc_wiatru < 10 TO warunki_na_trasie = 'dobre' 

Jaka jest prędkość wiatru (km/h)? (? = dlaczego pytam) 5 

Jakie jest Twoje zmęczenie? (brak/niewielkie/średnie/duże) (? = dlaczego pytam) brak 

Czy masz ochotę na wymagającą trasę? (tak/nie) (? = dlaczego pytam) ? 

Pytam, bo sprawdzam regułę: R1: JEŚLI warunki_na_trasie == 'dobre' ORAZ zmeczenie == 'brak' ORAZ ochota == 'tak' TO decyzja = 'całodniowa trasa' 

Czy masz ochotę na wymagającą trasę? (tak/nie) (? = dlaczego pytam) nie 

Polecam: długa trasa 

Reguły: P6 -> R2 

  

=== Jak doszedłem do wniosku? === 

1. P6: JEŚLI pogoda == 'pochmurna' ORAZ predkosc_wiatru < 10 TO warunki_na_trasie = 'dobre' 

   -> Pochmurno, ale prawie bezwietrznie, więc jedzie się dobrze (wyjątek ważniejszy niż P3). 

2. R2: JEŚLI warunki_na_trasie == 'dobre' ORAZ zmeczenie == 'brak' ORAZ ochota == 'nie' TO decyzja = 'długa trasa' 

   -> Dobre warunki i brak zmęczenia, ale bez ochoty na wymagającą trasę. 

Co to jest? Długi trening na dobrej formie.

## Dlaczego te pytania

Celem jest "decyzja", a każda reguła R zaczyna się od warunku "warunki_na_trasie", więc silnik najpierw ustala ten wniosek pośredni na podstawie pogody i wiatru. Dla pochmurnej pogody P1 i P2 odpada (wymagają one słonecznej pogody). Pierwszą regułą, która potrzebuje wiatru jest P6 - stąd pytanie o wiatr. Przy dobrych warunkach i braku zmęczenia decyzja zależy od ochoty, dlatego system o nią pyta.

## Kolejność reguł 

Gdy pasują dwie reguły, wygrywa ta, która stoi wyżej w pliku. Dlatego wyjątek P6 (pochmurno i wiatr < 10km/h) stoi przed P3.

## Weryfikacja bazy wiedzy

kawa_z_bledami.json: 6 błędów, 4 uwagi
kawa.json: 0 błędów, 0 uwag
trasa.json: 0 błędów, 0 uwag

## Uwagi i ograniczenia

- Weryfikator nie zgłosił żadnych uwag w trasa.json.
- Weryfikator nie wykrywa nakładanie się przedziałów P6 i P3. Konflikt rozstrzyga kolejność reguł.
- Weryfikacja dotyczy budowy bazy, nie trafności progów (zadanie eksperta)
- Ograniczenie w aplikacji: brak "dlaczego" w interfejsie (jest tylko w konsoli) 
