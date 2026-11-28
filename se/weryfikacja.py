"""Weryfikacja bazy wiedzy (odpowiednik programu Cake z pakietu SPHINX) — do uzupełnienia na spotkaniu 3.
Uruchom: python se/weryfikacja.py wiedza/kawa_z_bledami.json
"""
import sys
from pathlib import Path

from silnik import OPERATORY, wczytaj_baze


def weryfikuj(baza):
    """Zwraca listę (poziom, komunikat); poziom to 'BŁĄD' albo 'UWAGA'."""
    raport = []
    atrybuty = baza["atrybuty"]
    reguly = baza["reguly"]

    # Test 1 (gotowy): powtórzone identyfikatory reguł
    ids = [r["id"] for r in reguly]
    for id_ in sorted({i for i in ids if ids.count(i) > 1}):
        raport.append(("BŁĄD", f"Powtórzony identyfikator reguły {id_}"))

    # Test 2 (gotowy): niezadeklarowane atrybuty i nieznane operatory w warunkach
    for r in reguly:
        for atr, op, wart in r["jesli"]:
            if atr not in atrybuty:
                raport.append(("BŁĄD", f"{r['id']}: niezadeklarowany atrybut '{atr}'"))
            if op not in OPERATORY:
                raport.append(("BŁĄD", f"{r['id']}: nieznany operator '{op}'"))

    # TODO 3: wartości spoza dziedziny — dla atrybutów z listą "wartosci"
    #         sprawdź warunki z operatorem == lub != (BŁĄD).
    for r in reguly:
        for atr, op, wart in r["jesli"]:
            opis = atrybuty.get(atr)
            if op in("==", "!=") and opis and "wartosci" in opis and wart not in opis["wartosci"]:
                raport.append(("BŁĄD", f"{r['id']}: Wartość '{wart}' spoza dziedziny '{atr}'"))
    # TODO 4: nieużywane atrybuty wejściowe (typ inny niż "wniosek", nieobecne w żadnym warunku)
    #         oraz nieużywane wartości atrybutów typu "wybor" (UWAGA).
    uzyte_atrybuty = {atr for r in reguly for atr, op, wart in r["jesli"]}
    uzyte_wartosci = {(atr, wart) for r in reguly for atr, op, wart in r["jesli"]}
    for nazwa, opis in atrybuty.items():
        if opis["typ"] != "wniosek" and nazwa not in uzyte_atrybuty:
            raport.append(("UWAGA", f"Atrybut '{nazwa}' nie jest używany w żadnej regule"))
        if opis["typ"] == "wybor":
            for wartosc in opis["wartosci"]:
                if (nazwa, wartosc) not in uzyte_wartosci:
                    raport.append(("UWAGA", f"Wartość '{wartosc}' atrybutu '{nazwa}' nieużywana"))
    # TODO 5: warunek niemożliwy do spełnienia — warunek atr == wart, gdzie atr jest typu "wniosek",
    #         a żadna reguła nie ma wniosku ["atr", "wart"] (BŁĄD).
    wytwarzane = {tuple(r["to"]) for r in reguly}
    for r in reguly:
        for atr, op, wart in r["jesli"]:
            opis = atrybuty.get(atr)
            if op == "==" and opis and opis["typ"] == "wniosek" and (atr, wart) not in wytwarzane:
                raport.append(("BŁĄD", f"{r['id']} warunek {atr} == {wart} nigdy niespełniony"))
    # TODO 6: porównaj każdą parę reguł (warunki zamień na zbiory krotek: {tuple(w) for w in r["jesli"]}):
    #   - te same warunki i ten sam wniosek       -> duplikat (UWAGA)
    #   - te same warunki, inna wartość wniosku   -> sprzeczność (BŁĄD)
    #   - ten sam wniosek, warunki A ⊂ warunki B  -> B jest pochłaniana przez A (UWAGA)
    for i, r1 in enumerate(reguly):
        for r2 in reguly[i + 1:]:
            wa = {tuple(w) for w in r1["jesli"]}
            wb = {tuple(w) for w in r2["jesli"]}
            if wa == wb and r1["to"] == r2["to"]:
                raport.append(("UWAGA", f"{r1['id']} i {r2['id']} są identyczne (duplikat)"))
            elif wa == wb and r1["to"][0] == r2["to"][0]:
                raport.append(("BŁĄD", f"{r1['id']} i {r2['id']} są sprzeczne: te same warunki."))
            elif r1["to"] == r2["to"] and wa < wb:
                raport.append(("UWAGA", f"{r2['id']} pochłaniana przez {r1['id']} (zbędna)"))
            elif r1["to"] == r2["to"] and wb < wa:
                raport.append(("UWAGA", f"{r1['id']} pochłaniana przez {r2['id']} (zbędna)"))
    # TODO 7: cel główny baza["cel"] musi być wnioskiem co najmniej jednej reguły (BŁĄD).
    if not any(r["to"][0] == baza["cel"] for r in reguly):
        raport.append(("BŁĄD", f"{baza['cel']} nie jest wnioskiem żadnej reguły"))
    return raport


if __name__ == "__main__":
    plik = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent.parent / "wiedza" / "kawa.json"
    wyniki = weryfikuj(wczytaj_baze(plik))
    if not wyniki:
        print("Baza wiedzy nie zawiera wykrytych problemów.")
    for poziom, komunikat in wyniki:
        print(f"[{poziom}] {komunikat}")
    print(f"\nZnaleziono: {len(wyniki)} (w kawa_z_bledami.json jest 10 problemów do wykrycia)")
