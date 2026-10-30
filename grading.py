import math

AUSBILDUNGEN = {
    "bm": [
        {"id": "deutsch", "name": "Deutsch", "pruefung": True},
        {"id": "franzoesisch", "name": "Französisch", "pruefung": True},
        {"id": "englisch", "name": "Englisch", "pruefung": True},
        {"id": "mathe", "name": "Mathematik", "pruefung": True},
        {"id": "frw", "name": "Finanz- und Rechnungswesen", "pruefung": True},
        {"id": "wr", "name": "Wirtschaft und Recht", "pruefung": True},
        {"id": "gp", "name": "Geschichte und Politik", "pruefung": False},
        {"id": "tu", "name": "Technik und Umwelt", "pruefung": False},
        {"id": "idpa", "name": "IDPA", "pruefung": False},
    ],
}

REGELN = {
    "min_gesamt": 4.0, # Gesamtnote mindestens 4.0
    "max_unter_4": 2,  # Höchstens 2 Fachnoten unter 4
    "max_abweichung": 2.0, # Summe der Abweichungen unter 4 höchstens 2.0
}


def runde_halbe(note):
    return math.floor(note * 2 + 0.5) / 2


def runde_zehntel(note):
    return math.floor(note * 10 + 0.5 + 1e-9) / 10


def fachnote(erfahrungsnote, pruefungsnote):
    if erfahrungsnote is None:
        return None
    if pruefungsnote is None:
        return runde_halbe(erfahrungsnote)
    return runde_halbe((erfahrungsnote + pruefungsnote) / 2)


def berechne(noten):
    fachnoten = {}
    for fach in noten:
        note = fachnote(fach["erfahrungsnote"], fach["pruefungsnote"])
        if note is not None:
            fachnoten[fach["name"]] = note

    if not fachnoten:
        return None

    werte = list(fachnoten.values())
    gesamtnote = runde_zehntel(sum(werte) / len(werte))
    unter_4 = [n for n in werte if n < 4]
    abweichung = sum(4 - n for n in unter_4)

    gruende = []
    if gesamtnote < REGELN["min_gesamt"]:
        gruende.append(f"Gesamtnote {gesamtnote} ist unter 4.0")
    if len(unter_4) > REGELN["max_unter_4"]:
        gruende.append(f"{len(unter_4)} Fachnoten unter 4 (max. 2)")
    if abweichung > REGELN["max_abweichung"]:
        gruende.append(f"Abweichung unter 4 ist {abweichung} (max. 2.0)")

    return {
        "fachnoten": fachnoten,
        "gesamtnote": gesamtnote,
        "bestanden": len(gruende) == 0,
        "gruende": gruende,
    }