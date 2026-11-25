from pathlib import Path

from silnik import wczytaj_baze, wnioskuj_w_przod, wnioskuj_wstecz

baza = wczytaj_baze(Path(__file__).parent.parent / "wiedza" / "trasa.json")

PRZYPADKI = [
    ({"pogoda": "słoneczna", "predkosc_wiatru": 20, "zmeczenie": "niewielkie", "ochota": "tak"},
     "długa trasa", ["P1", "R3"], "typowy przypadek"),
    ({"pogoda": "słoneczna", "predkosc_wiatru": 30, "zmeczenie": "brak", "ochota": "tak"},
     "brak trasy", ["P2", "R15"], "próg: wiatr dokładnie 30 (>= 30 to złe)"),
    ({"pogoda": "słoneczna", "predkosc_wiatru": 29, "zmeczenie": "brak", "ochota": "tak"},
     "całodniowa trasa", ["P1", "R1"], "tuż pod progiem: wiatr 29"),
    ({"pogoda": "deszczowa", "predkosc_wiatru": 5, "zmeczenie": "brak", "ochota": "tak"},
     "brak trasy", ["P5", "R15"], "deszcz kończy sprawę"),
    ({"pogoda": "pochmurna", "predkosc_wiatru": 5, "zmeczenie": "brak", "ochota": "nie"},
     "długa trasa", ["P6", "R2"], "konkurencja: pasują P6 i P3, wygrywa P6 (stoi wyżej)"),
    ({"pogoda": "pochmurna", "predkosc_wiatru": 10, "zmeczenie": "brak", "ochota": "nie"},
     "średnia trasa", ["P3", "R9"], "próg P6: wiatr 10 nie jest < 10, więc P3"),
    ({"pogoda": "słoneczna", "predkosc_wiatru": 20, "ochota": "tak"},
     None, None, "bez wyniku: brak danych o zmęczeniu"),
]

ok = 0
for wejscie, oczekiwane, oczekiwany_slad, opis in PRZYPADKI:
    fakty, slad = wnioskuj_w_przod(baza, wejscie)
    w_przod_ok = fakty.get("decyzja") == oczekiwane and (oczekiwany_slad is None or slad == oczekiwany_slad)

    zadane = []
    def zapytaj(atrybut, powod):
        zadane.append(atrybut)
        return wejscie.get(atrybut)
    wstecz = wnioskuj_wstecz(baza, "decyzja", {}, zapytaj, [])
    wstecz_ok = wstecz == oczekiwane and len(zadane) == len(set(zadane))

    status = "OK " if w_przod_ok and wstecz_ok else "BŁĄD"
    ok += w_przod_ok and wstecz_ok
    print(f"[{status}] {wejscie} -> w przód: {fakty.get('decyzja')}, wstecz: {wstecz}, pytań: {len(zadane)}")

print(f"\nZaliczone przypadki: {ok}/{len(PRZYPADKI)}")
