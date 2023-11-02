# darlehenpy

Ein kleines Paket zur Berechnung von Darlehen. Bei weitem (noch 😉) nicht so mächtig wie z.B. der [Hypothekenrechner](https://www.zinsen-berechnen.de/hypothekenrechner.php).

Es wird zwischen der Berechnung basierend auf der Monatsrate oder basierend auf der anfänglichen Tilgungsrate unterschieden. Die Angabe einer jährlichen Sondertilgung ist auch möglich.

[Projekt auf PyPI](https://pypi.org/project/darlehen.py/)

## Quickstart

```
pip install darlehen.py
import darlehenpy.darlehen as darlehen
darlehen.berechne_mit_monatsrate(...)
darlehen.berechne_mit_tilgungsrate(...)
```

**Achtung!** Punkt als Dezimaltrennzeichen!

## Beispiel

Aus der [beispiel.py](https://github.com/Allaman/darlehenpy/blob/main/beispiel.py).

```python
import src.darlehenpy.darlehen as darlehen
# Die Ausgabe kann man schöner machen ;)

# Rahmenbedingungen
P = 100000
i = 4.1
n = 10
S = 5000

print(
    f"Darlehensumme: {P} €\nZinssatz (p.a.): {i} %\nLaufzeit: {n} Jahre\nSondertilung (p.a.): {S}\n"
)

# Berechnung basierend auf einer Monatsrate
M = 500
print(f"Monatsrate: {M} €")
t0, R, gesamtaufwand, jahr, monat = darlehen.berechne_mit_monatsrate(P, i, M, n, S)
print(
    f"Anfängliche Tilgungsrate: {t0} %\nRestschuld nach {n} Jahren: {R} €\nGesamtaufwand: {gesamtaufwand} €\nAbbezahlt im {jahr}. Jahr und {monat}. Monat\n"
)

# Berechnung basierend auf der anfänglichen Tilgungsrate
t0 = 5.5
print(f"Anfängliche Tilgungsrate: {t0} %")
M, R, gesamtaufwand, jahr, monat = darlehen.berechne_mit_tilgungsrate(P, i, t0, n, S)
print(
    f"Monatsrate: {M} €\nRestschuld nach {n} Jahren: {R} €\nGesamtaufwand: {gesamtaufwand} €\nAbbezahlt im {jahr}. Jahr und {monat}. Monat"
)
```

Ausgabe:

```
❯ python test.py
Darlehensumme: 100000 €
Zinssatz (p.a.): 4.1 %
Laufzeit: 10 Jahre
Sondertilung (p.a.): 5000

Monatsrate: 500 €
Anfängliche Tilgungsrate: 1.9 %
Restschuld nach 10 Jahren: 16033.91 €
Gesamtaufwand: 126033.91 €
Abbezahlt im None. Jahr und None. Monat

Anfängliche Tilgungsrate: 5.5 %
Monatsrate: 800.0 €
Restschuld nach 10 Jahren: 0.0 €
Gesamtaufwand: 118474.63 €
Abbezahlt im 9. Jahr und 3. Monat
```

Man kann sich damit natürlich viele Werte auf einmal berechnen lassen und vergleichen. Z.B. mit einer CSV mit folgenden Spalten als Input:

```csv
P,i,M,n,S,
```

bzw.

```
P,i,t0,n,S,
```

## Tests

Eine Testmatrix mit Werten ermittelt aus dem [Hypothekenrechner](https://www.zinsen-berechnen.de/hypothekenrechner.php) testet die berechneten Ergebnisse.

**Es kann keine Gewährleistung für die von diesem Paket berechneten Ergebnisse übernommen werden**
