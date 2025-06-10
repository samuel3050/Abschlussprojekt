from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Spielfeld: 11x11, nur äußere Felder im Uhrzeigersinn (40 Felder)
felder = (
    [(x, 0) for x in range(11)] +
    [(10, y) for y in range(1, 11)] +
    [(x, 10) for x in range(9, -1, -1)] +
    [(0, y) for y in range(9, 0, -1)]
)

# --- NEU: Felderinfos für Kauf/Miete (Dummy-Daten, später aus DB laden) ---
felder_infos = [
    {"name": f"Feld {i}", "kaufpreis": 100 + i*10, "miete": 20 + i*2, "besitzer": None}
    for i in range(len(felder))
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["anzahl"] = int(request.form["anzahl"])
        return redirect("/namen")
    return render_template("index.html")

@app.route("/namen", methods=["GET", "POST"])
def namen():
    if request.method == "POST":
        spieler = [request.form[f"spieler{i}"] for i in range(1, session["anzahl"] + 1)]
        session["spieler"] = spieler
        session["aktiver"] = 0
        session["positionen"] = [0] * len(spieler)  # Positionen pro Spieler
        session["gesamt"] = [0] * len(spieler)
        session["wurf"] = None
        return redirect("/board")
    return render_template("spielernamen.html", anzahl=session["anzahl"])

@app.route("/board", methods=["GET", "POST"])
def spiel():
    # Session-Absicherung
    if "spieler" not in session or "positionen" not in session or "aktiver" not in session:
        return redirect(url_for("index"))

    feldinfo = None
    zeige_feldinfo = False

    if request.method == "POST":
        würfel1 = random.randint(1, 6)
        würfel2 = random.randint(1, 6)
        summe = würfel1 + würfel2
        aktiver = session["aktiver"]

        # Spielerposition aktualisieren
        pos_liste = session["positionen"]
        neue_pos = (pos_liste[aktiver] + summe) % len(felder)
        pos_liste[aktiver] = neue_pos
        session["positionen"] = pos_liste

        # Gesamtwurf-Zahl speichern
        session["gesamt"][aktiver] += summe
        session["wurf"] = (würfel1, würfel2)

        # Feldinfo für Overlay merken und Flag setzen
        session["feldinfo"] = felder_infos[neue_pos]
        session["zeige_feldinfo"] = True

        # Immer zum nächsten Spieler wechseln
        session["aktiver"] = (aktiver + 1) % len(session["spieler"])

        return redirect("/board")

    # GET: Board anzeigen
    aktiver = session.get("aktiver", 0)
    pos_liste = session.get("positionen", [])

    # Feldinfo und Flag nur anzeigen, wenn nach Bewegung (Flag gesetzt)
    if session.get("zeige_feldinfo"):
        feldinfo = session.get("feldinfo")
        zeige_feldinfo = True
        # Flag zurücksetzen, damit es nur einmal angezeigt wird
        session["zeige_feldinfo"] = False
    else:
        feldinfo = None
        zeige_feldinfo = False

    return render_template(
        "board.html",
        felder=felder,
        spieler=session.get("spieler", []),
        positionen=pos_liste,
        aktiver=aktiver,
        wurf=session.get("wurf"),
        feldinfo=feldinfo,
        zeige_feldinfo=zeige_feldinfo
    )

if __name__ == "__main__":
    print("🟢 Spiel gestartet auf Feld 0")
    app.run(debug=True)