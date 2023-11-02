# vim: foldmethod=indent


def berechne_mit_monatsrate(P, i, M, n, S):
    """Berechne ein Darlehen basierend auf der Monatsrate

    Args:
        P (decimal): Darlehensbetrag in Euro
        i (decimal): Zinssatz in %
        M (decimal): monatliche Rückzahlungsrate in Euro
        n (integer): Laufzeit in Jahren
        S (decimal): Jährliche Sondertilgung in Euro

    Returns:
        to (decimal): Den anfänglichen Tilgungssatz
        R (decimal): Die Restschuld in Euro
        gesamtaufwand (decimal): Die Summe aus Darlehen plus Zinsen
        schuld_abbezahlt_jahr (integer): Das Jahr in dem die Schulden abbezahlt wurden oder None
        schuld_abbezahlt_monat (integer): Der Monat in dem die Schulden abbezahlt wurden oder None
    """
    r_m = (i / 100) / 12  # Monatlicher Zinssatz

    zins_erster_monat = P * r_m
    tilgung_erster_monat = M - zins_erster_monat
    tilgung_erstes_jahr = 12 * tilgung_erster_monat
    t0 = (tilgung_erstes_jahr / P) * 100  # Anfängliche Tilgungsrate in Prozent

    R = P  # aktuelle Restschuld
    gesamtaufwand = P  # Summe aller bisherigen Zahlungen inklusive Darlehensbetrag

    schuld_abbezahlt_jahr = None
    schuld_abbezahlt_monat = None

    for jahr in range(n):
        for monat in range(12):
            zins = R * r_m  # Zins für aktuellen Monat

            gesamtaufwand += zins  # Addiere Zins zum gesamtaufwand

            monatszahlung = min(
                M, zins + R
            )  # Entweder die ganze Monatsrate oder nur das, was benötigt wird
            tilgung = monatszahlung - zins
            R -= tilgung  # Restschuld reduzieren

            # Wenn Restschuld negativ oder 0, Speicherdatum und Beendeschleifen
            if R <= 0 and schuld_abbezahlt_jahr is None:
                schuld_abbezahlt_jahr = jahr + 1
                schuld_abbezahlt_monat = monat + 1
                break

        # Sondertilgung am Ende des Jahres, wenn noch eine Restschuld vorhanden ist
        if R > 0:
            sondertilgung = min(
                S, R
            )  # Füge entweder volle Sondertilgung hinzu oder was von R übrig ist
            R -= sondertilgung

        # Wenn Restschuld nach Sondertilgung abbezahlt ist
        if R <= 0 and schuld_abbezahlt_jahr is None:
            schuld_abbezahlt_jahr = jahr + 1
            break

    return (
        round(t0, 2),
        round(R, 2),
        round(gesamtaufwand, 2),
        schuld_abbezahlt_jahr,
        schuld_abbezahlt_monat,
    )


def berechne_mit_tilgungsrate(P, i, t0, n, S):
    """Berechne ein Darlehen basierend auf der anfänglichen Tilgungsrate

    Args:
        P (decimal): Der Darlehensbetrag in Euro
        i (decimal): Der Zinssatz in %
        t0 (decimal): Die anfängliche Tilgungsrate in %
        n (integer): Die Laufzeit in Jahren
        S (decimal): Jährliche Sondertilgung in Euro

    Returns:
        M (decimal): Die monatliche Rate in Euro
        R (decimal): Die Restschuld in Euro
        gesamtaufwand (decimal): Die Summe aus Darlehen plus Zinsen
        schuld_abbezahlt_jahr (integer): Das Jahr in dem die Schulden abbezahlt wurden oder None
        schuld_abbezahlt_monat (integer): Der Monat in dem die Schulden abbezahlt wurden oder None
    """
    r_m = (i / 100) / 12  # Monatlicher Zinssatz
    t0_m = (t0 / 100) * P / 12  # Anfängliche monatliche Tilgung in Euro
    M = P * r_m + t0_m  # Monatliche Rate basierend auf anfänglicher Tilgungsrate

    R = P
    gesamtaufwand = P  # Zu Beginn setzen wir gesamtaufwand gleich dem Darlehensbetrag P
    schuld_abbezahlt_jahr = None
    schuld_abbezahlt_monat = None

    for jahr in range(n):
        for monat in range(12):
            zins = R * r_m  # Zins für aktuellen Monat

            gesamtaufwand += zins  # Addiere Zins zum gesamtaufwand

            monatszahlung = min(
                M, zins + R
            )  # Entweder die ganze Monatsrate oder nur das, was benötigt wird
            tilgung = monatszahlung - zins
            R -= tilgung  # Restschuld reduzieren

            # Wenn Restschuld negativ oder 0, Speicherdatum und Schleife beenden
            if (
                R <= 0 and schuld_abbezahlt_jahr is None
            ):  # Speichert das Jahr und den Monat, in dem die Schuld abbezahlt wurde
                schuld_abbezahlt_jahr = jahr + 1
                schuld_abbezahlt_monat = monat + 1
                break

        # Sondertilgung am Ende des Jahres, wenn noch eine Restschuld vorhanden ist
        if R > 0:
            sondertilgung = min(
                S, R
            )  # Füge entweder volle Sondertilgung hinzu oder was von R übrig ist
            R -= sondertilgung

        # Wenn Restschuld nach Sondertilgung abbezahlt ist
        if R <= 0 and schuld_abbezahlt_jahr is None:
            schuld_abbezahlt_jahr = jahr + 1
            break

    return (
        round(M, 2),
        round(R, 2),
        round(gesamtaufwand, 2),
        schuld_abbezahlt_jahr,
        schuld_abbezahlt_monat,
    )
