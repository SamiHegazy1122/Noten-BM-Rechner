from flask import Flask, render_template, request
from grading import KATEGORIEN, berechne

app = Flask(__name__)


def lese_note(feldname):
    wert = request.form.get(feldname, "").strip().replace(",", ".")
    try:
        return float(wert)
    except ValueError:
        return None


@app.route("/")
def index():
    return render_template("index.html", kategorien=KATEGORIEN)


@app.route("/<kategorie>", methods=["GET", "POST"])
def rechner(kategorie):
    if kategorie not in KATEGORIEN:
        return "Kategorie nicht gefunden", 404

    info = KATEGORIEN[kategorie]
    resultat = None

    if request.method == "POST":
        noten = []
        for i, fach in enumerate(info["faecher"]):
            noten.append({
                "name": fach["name"],
                "erfahrungsnote": lese_note(f"e{i}"),
                "pruefungsnote": lese_note(f"p{i}"),
            })
        resultat = berechne(noten, info["regel"])

    return render_template("rechner.html", info=info, resultat=resultat)


if __name__ == "__main__":
    app.run(debug=True)