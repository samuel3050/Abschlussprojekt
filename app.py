# Flask ist ein leichtgewichtiges Web-Framework in Python – wird hier importiert
from flask import Flask, render_template, request, redirect, session, url_for
import random  # Für das Zufallswürfeln (Würfel 1–6)

# Initialisierung der Flask-Anwendung
app = Flask(__name__)

# Geheimer Schlüssel für die Sitzung (Session), nötig für sichere Speicherung
app.secret_key = "supersecretkey"  # Dieser Schlüssel sollte in echten Projekten sicher gespeichert werden

# -------------------------------------------
# ROUTE 1: Startseite – Spieleranzahl festlegen
# -------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Die eingegebene Spieleranzahl (als String) wird in int umgewandelt
        # und in der Server-Session gespeichert (bleibt über Seiten hinweg erhalten)
        session["anzahl"] = int(request.form["anzahl"])
        
        # Nach erfolgreicher Eingabe wird zur nächsten Seite weitergeleitet
        return redirect("/namen")

    # Wenn GET-Anfrage: HTML-Seite anzeigen, auf der man die Spieleranzahl auswählt
    return render_template("index.html")

# -------------------------------------------
# ROUTE 2: Namen der Spieler eingeben
# -------------------------------------------
@app.route("/namen", methods=["GET", "POST"])
def namen():
    if request.method == "POST":
        # Eine Liste der Spielernamen wird aus den Formularfeldern ausgelesen.
        # Das Feld heißt jeweils "spieler1", "spieler2", usw.
        spieler = [request.form[f"spieler{i}"] for i in range(1, session["anzahl"] + 1)]

        # Namen in der Session speichern
        session["spieler"] = spieler

        # Index für den aktuell aktiven Spieler (zuerst Spieler 0)
        session["aktiver"] = 0

        # Liste für Gesamtpunktestand: Jeder Spieler startet mit 0 Punkten
        session["gesamt"] = [0] * len(spieler)

        # Weiterleitung zur Würfelseite
        return redirect("/dice")

    # Wenn GET-Anfrage: Formular anzeigen mit Feldern für jeden Spielernamen
    # Die Anzahl wird aus der Session gelesen
    return render_template("spielernamen.html", anzahl=session["anzahl"])

# -------------------------------------------
# ROUTE 3: Würfelseite anzeigen
# -------------------------------------------
@app.route("/dice")
def dice():
    # Aus der Session: Liste aller Spielernamen laden
    spieler = session.get("spieler", [])

    # Aus der Session: Welcher Spieler ist aktuell dran? (Index)
    aktiver = session.get("aktiver", 0)

    # HTML-Vorlage anzeigen und Spielernamen + aktiven Spieler übergeben
    return render_template("dice.html", spieler=spieler, aktiver=aktiver)

# -------------------------------------------
# ROUTE 4: API-Endpunkt zum Würfeln (JavaScript ruft diesen auf)
# -------------------------------------------
@app.route("/roll")
def roll():
    # Würfelzahl für Würfel 1 und 2 generieren (Zufallszahlen zwischen 1 und 6)
    würfel1 = random.randint(1, 6)
    würfel2 = random.randint(1, 6)

    # Die Augensumme beider Würfel berechnen
    summe = würfel1 + würfel2

    # Prüfen, ob ein Doppelwurf (z. B. zwei Sechsen) vorliegt
    doppel = würfel1 == würfel2

    # Aktuellen Spielerindex aus der Session laden
    aktiver = session["aktiver"]

    # Die Summe wird zum Punktestand des aktuellen Spielers addiert
    session["gesamt"][aktiver] += summe

    # Wenn NICHT doppelt gewürfelt wurde → nächster Spieler ist dran
    if not doppel:
        session["aktiver"] = (aktiver + 1) % len(session["spieler"])
        # Durch Modulo geht es nach dem letzten Spieler wieder zu Spieler 0

    # Rückgabe eines JSON-Objekts (für JavaScript in der dice.html)
    return {
        "w1": würfel1,                        # Erster Würfel
        "w2": würfel2,                        # Zweiter Würfel
        "summe": summe,                      # Augensumme
        "doppel": doppel,                    # Boolean: doppelt gewürfelt?
        "spieler": session["spieler"][session["aktiver"]],  # Nächster Spieler
        "gesamt": session["gesamt"]          # Punktestände aller Spieler
    }

# -------------------------------------------
# Programmstart (wenn Datei direkt ausgeführt wird)
# -------------------------------------------
if __name__ == "__main__":
    # Starte lokalen Entwicklungsserver mit automatischem Reload bei Änderungen
    app.run(debug=True)
