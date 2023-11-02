"""Beinhaltet die Funktionalität"""


# pylint: disable-next=too-many-locals
def berechne_mit_monatsrate(
    darlehenssumme, zinssatz, monatsrate, laufzeit, sondertilgung
):
    """Berechne ein Darlehen basierend auf der Monatsrate

    Args:
        darlehenssumme (decimal): Darlehensbetrag in Euro
        zinssatz (decimal): Zinssatz in %
        monatsrate (decimal): monatliche Rückzahlungsrate in Euro
        laufzeit (integer): Laufzeit in Jahren
        sondertilgung (decimal): Jährliche Sondertilgung in Euro

    Returns:
        t0 (decimal): Den anfänglichen Tilgungssatz
        R (decimal): Die Restschuld in Euro
        gesamtaufwand (decimal): Die Summe aus Darlehen plus Zinsen
        schuld_abbezahlt_jahr (integer): Das Jahr in dem die Schulden abbezahlt wurden oder None
        schuld_abbezahlt_monat (integer): Der Monat in dem die Schulden abbezahlt wurden oder None
    """
    r_m = (zinssatz / 100) / 12  # Monatlicher Zinssatz

    zins_erster_monat = darlehenssumme * r_m
    tilgung_erster_monat = monatsrate - zins_erster_monat
    tilgung_erstes_jahr = 12 * tilgung_erster_monat
    t0 = (
        tilgung_erstes_jahr / darlehenssumme
    ) * 100  # Anfängliche Tilgungsrate in Prozent

    restschuld = darlehenssumme  # aktuelle Restschuld
    gesamtaufwand = (
        darlehenssumme  # Summe aller bisherigen Zahlungen inklusive Darlehensbetrag
    )

    schuld_abbezahlt_jahr = None
    schuld_abbezahlt_monat = None

    for jahr in range(laufzeit):
        for monat in range(12):
            zins = restschuld * r_m  # Zins für aktuellen Monat

            gesamtaufwand += zins  # Addiere Zins zum gesamtaufwand

            monatszahlung = min(
                monatsrate, zins + restschuld
            )  # Entweder die ganze Monatsrate oder nur das, was benötigt wird
            tilgung = monatszahlung - zins
            restschuld -= tilgung  # Restschuld reduzieren

            # Wenn Restschuld negativ oder 0, datum speichern und loop beenden
            if restschuld <= 0 and schuld_abbezahlt_jahr is None:
                schuld_abbezahlt_jahr = jahr + 1
                schuld_abbezahlt_monat = monat + 1
                break

        # Sondertilgung am Ende des Jahres, wenn noch eine Restschuld vorhanden ist
        if restschuld > 0:
            sondertilgung = min(
                sondertilgung, restschuld
            )  # Füge entweder volle Sondertilgung hinzu oder was von der Restschuld übrig ist
            restschuld -= sondertilgung

        # Wenn Restschuld nach Sondertilgung abbezahlt ist
        if restschuld <= 0 and schuld_abbezahlt_jahr is None:
            schuld_abbezahlt_jahr = jahr + 1
            break

    return (
        round(t0, 2),
        round(restschuld, 2),
        round(gesamtaufwand, 2),
        schuld_abbezahlt_jahr,
        schuld_abbezahlt_monat,
    )


# pylint: disable-next=too-many-locals
def berechne_mit_tilgungsrate(
    darlehenssumme, zinssatz, tilgungsrate, nlaufzeit, sondertilgung
):
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
    r_m = (zinssatz / 100) / 12  # Monatlicher Zinssatz
    t0_m = (
        (tilgungsrate / 100) * darlehenssumme / 12
    )  # Anfängliche monatliche Tilgung in Euro
    monatsrate = (
        darlehenssumme * r_m + t0_m
    )  # Monatliche Rate basierend auf anfänglicher Tilgungsrate

    restschuld = darlehenssumme
    gesamtaufwand = (
        darlehenssumme  # Zu Beginn setzen wir gesamtaufwand gleich dem Darlehensbetrag
    )
    schuld_abbezahlt_jahr = None
    schuld_abbezahlt_monat = None

    for jahr in range(nlaufzeit):
        for monat in range(12):
            zins = restschuld * r_m  # Zins für aktuellen Monat

            gesamtaufwand += zins  # Addiere Zins zum gesamtaufwand

            monatszahlung = min(
                monatsrate, zins + restschuld
            )  # Entweder die ganze Monatsrate oder nur das, was benötigt wird
            tilgung = monatszahlung - zins
            restschuld -= tilgung  # Restschuld reduzieren

            # Wenn Restschuld negativ oder 0, Speicherdatum und Schleife beenden
            if (
                restschuld <= 0 and schuld_abbezahlt_jahr is None
            ):  # Speichert das Jahr und den Monat, in dem die Schuld abbezahlt wurde
                schuld_abbezahlt_jahr = jahr + 1
                schuld_abbezahlt_monat = monat + 1
                break

        # Sondertilgung am Ende des Jahres, wenn noch eine Restschuld vorhanden ist
        if restschuld > 0:
            sondertilgung = min(
                sondertilgung, restschuld
            )  # Füge entweder volle Sondertilgung hinzu oder was von der Restschuld übrig ist
            restschuld -= sondertilgung

        # Wenn Restschuld nach Sondertilgung abbezahlt ist
        if restschuld <= 0 and schuld_abbezahlt_jahr is None:
            schuld_abbezahlt_jahr = jahr + 1
            break

    return (
        round(monatsrate, 2),
        round(restschuld, 2),
        round(gesamtaufwand, 2),
        schuld_abbezahlt_jahr,
        schuld_abbezahlt_monat,
    )


# vim: foldmethod=indent
