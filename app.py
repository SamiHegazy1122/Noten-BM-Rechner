from flask import Flask, render_template, request
from grading import AUSBILDUNGEN, berechne

app = Flask(__name__)


def lese_note(feldname):
    wert = request.form.get(feldname, "").strip().replace(",", ".")
    return float(wert) if wert else None


@app.route("/")
def index():
    return render_template("index.html", ausbildungen=AUSBILDUNGEN.keys())


@app.route("/<ausbildung>", methods=["GET", "POST"])
def rechner(ausbildung):
    if ausbildung not in AUSBILDUNGEN:
        return "Ausbildung nicht gefunden", 404

    faecher = AUSBILDUNGEN[ausbildung]
    resultat = None

    if request.method == "POST":
        noten = []
        for fach in faecher:
            noten.append({
                "name": fach["name"],
                "erfahrungsnote": lese_note(fach["id"] + "_erfahrung"),
                "pruefungsnote": lese_note(fach["id"] + "_pruefung"),
            })
        resultat = berechne(noten)

    return render_template(
        "rechner.html",
        ausbildung=ausbildung,
        faecher=faecher,
        resultat=resultat,
    )


if __name__ == "__main__":
    app.run(debug=True)