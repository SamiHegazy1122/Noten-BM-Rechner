import math


def fach(name, pruefung=False):
    return {"name": name, "pruefung": pruefung}


# Fächer aus dem Kanton Aargau
KATEGORIEN = {
    "gymnasium": {
        "name": "Gymnasium (Kanti)",
        "abschluss": "Gymnasiale Maturität",
        "gruppe": "Mittelschule",
        "regel": "matur",
        "faecher": [
            fach("Deutsch", True),
            fach("Französisch", True),
            fach("Englisch", True),
            fach("Mathematik", True),
            fach("Biologie"),
            fach("Chemie"),
            fach("Physik"),
            fach("Geschichte"),
            fach("Geografie"),
            fach("Bildnerisches Gestalten / Musik"),
            fach("Schwerpunktfach", True),
            fach("Ergänzungsfach"),
            fach("Maturaarbeit"),
        ],
    },
    "wms": {
        "name": "WMS",
        "abschluss": "Wirtschaftsmittelschule – BM Wirtschaft",
        "gruppe": "Mittelschule",
        "regel": "bm",
        "faecher": [
            fach("Deutsch", True),
            fach("Französisch", True),
            fach("Englisch", True),
            fach("Mathematik", True),
            fach("Finanz- und Rechnungswesen", True),
            fach("Wirtschaft und Recht", True),
            fach("Geschichte und Politik"),
            fach("Technik und Umwelt"),
            fach("Interdisziplinäres Arbeiten (IDAF/IDPA)"),
        ],
    },
    "ims": {
        "name": "IMS",
        "abschluss": "Informatikmittelschule – BM Wirtschaft",
        "gruppe": "Mittelschule",
        "regel": "bm",
        "faecher": [
            fach("Deutsch", True),
            fach("Französisch", True),
            fach("Englisch", True),
            fach("Mathematik", True),
            fach("Finanz- und Rechnungswesen", True),
            fach("Wirtschaft und Recht", True),
            fach("Geschichte und Politik"),
            fach("Technik und Umwelt"),
            fach("Interdisziplinäres Arbeiten (IDAF/IDPA)"),
        ],
    },
    "fms": {
        "name": "FMS",
        "abschluss": "Fachmittelschulausweis",
        "gruppe": "Mittelschule",
        "regel": "fms",
        "faecher": [
            fach("Deutsch", True),
            fach("Französisch", True),
            fach("Englisch", True),
            fach("Mathematik", True),
            fach("Biologie"),
            fach("Chemie"),
            fach("Physik"),
            fach("Geschichte"),
            fach("Geografie"),
            fach("Berufsfeldfach", True),
            fach("Selbständige Arbeit"),
        ],
    },
    "bm-wirtschaft": {
        "name": "BM Wirtschaft",
        "abschluss": "Berufsmaturität für Lernende (BM1/BM2)",
        "gruppe": "Berufslehre",
        "regel": "bm",
        "faecher": [
            fach("Deutsch", True),
            fach("Französisch", True),
            fach("Englisch", True),
            fach("Mathematik", True),
            fach("Finanz- und Rechnungswesen", True),
            fach("Wirtschaft und Recht", True),
            fach("Geschichte und Politik"),
            fach("Technik und Umwelt"),
            fach("Interdisziplinäres Arbeiten (IDAF/IDPA)"),
        ],
    },
    "bm-technik": {
        "name": "BM Technik",
        "abschluss": "Berufsmaturität für Lernende (BM1/BM2)",
        "gruppe": "Berufslehre",
        "regel": "bm",
        "faecher": [
            fach("Deutsch", True),
            fach("Französisch", True),
            fach("Englisch", True),
            fach("Mathematik", True),
            fach("Naturwissenschaften", True),
            fach("Geschichte und Politik"),
            fach("Wirtschaft und Recht"),
            fach("Interdisziplinäres Arbeiten (IDAF/IDPA)"),
        ],
    },
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


def pruefe_regeln(regel, werte, durchschnitt):
    unter_4 = [n for n in werte if n < 4]
    minus = sum(4 - n for n in unter_4)
    plus = sum(n - 4 for n in werte if n > 4)

    if regel == "matur":
        return [
            ("Höchstens 4 Noten unter 4", len(unter_4) <= 4),
            ("Minuspunkte doppelt kompensiert", 2 * minus <= plus),
        ]

    max_unter_4 = 3 if regel == "fms" else 2
    return [
        ("Durchschnitt mindestens 4.0", durchschnitt >= 4),
        (f"Höchstens {max_unter_4} Noten unter 4", len(unter_4) <= max_unter_4),
        ("Minuspunkte höchstens 2.0", minus <= 2),
    ]


def berechne(noten, regel):
    # noten = [{"name": "Deutsch", "erfahrungsnote": 4.5, "pruefungsnote": 5.0}, ...]
    fachnoten = {}
    for f in noten:
        note = fachnote(f["erfahrungsnote"], f["pruefungsnote"])
        if note is not None:
            fachnoten[f["name"]] = note

    if not fachnoten:
        return None

    werte = list(fachnoten.values())
    durchschnitt = runde_zehntel(sum(werte) / len(werte))
    regeln = pruefe_regeln(regel, werte, durchschnitt)

    return {
        "fachnoten": fachnoten,
        "durchschnitt": durchschnitt,
        "regeln": regeln,
        "bestanden": all(ok for _, ok in regeln),
        "ausgefuellt": len(fachnoten),
        "total": len(noten),
    }