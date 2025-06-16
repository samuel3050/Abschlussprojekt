from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Spielfeld: 11x11, nur äußere Felder im Uhrzeigersinn (40 Felder)
felder = (
    [(x, 0) for x in range(11)] +
    [(10, y) for y in range(1, 11)] +
    [(x, 10) for x in range(9, -1, -1)] +
    [(0, y) for y in range(9, 0, -1)]
)

def lade_felder_infos():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="saufmonopoly"  # Name wie im Screenshot
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM spielfelder ORDER BY feld_id ASC")
    felder_db = cursor.fetchall()
    cursor.close()
    conn.close()
    # Fehlerbehandlung: Prüfe, ob 40 Felder vorhanden sind
    if len(felder_db) < 40:
        raise Exception(f"Es wurden nur {len(felder_db)} Felder gefunden! Die Datenbank muss 40 Felder enthalten.")
    return felder_db

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
        session["konto"] = [30] * len(spieler)  # Jeder startet mit 30 Schlucken (Beispiel)
        session["wurf"] = None
        return redirect("/board")
    return render_template("spielernamen.html", anzahl=session["anzahl"])

@app.route("/board", methods=["GET", "POST"])
def spiel():
    # Session-Absicherung
    if "spieler" not in session or "positionen" not in session or "aktiver" not in session:
        return redirect(url_for("index"))

    # Felderinfos aus DB laden
    felder_infos = lade_felder_infos()

    feldinfo = None
    zeige_feldinfo = False

    if request.method == "POST":
        würfel1 = random.randint(1, 6)
        würfel2 = random.randint(1, 6)
        summe = würfel1 + würfel2
        aktiver = session["aktiver"]

        # Spielerposition aktualisieren
        pos_liste = session["positionen"]
        neue_pos = (pos_liste[aktiver] + summe) % len(felder_infos)
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

    # Felderinfos aus DB laden (erneut, damit immer aktuell)
    felder_infos = lade_felder_infos()

    # Feldinfo und Flag nur anzeigen, wenn nach Bewegung (Flag gesetzt)
    if session.get("zeige_feldinfo"):
        feldinfo = session.get("feldinfo")
        zeige_feldinfo = True
        session["zeige_feldinfo"] = False
    else:
        feldinfo = None
        zeige_feldinfo = False

    return render_template(
        "board.html",
        felder=[(f["feld_id"]-1) for f in felder_infos],  # für das Grid
        spieler=session.get("spieler", []),
        positionen=pos_liste,
        aktiver=aktiver,
        wurf=session.get("wurf"),
        feldinfo=feldinfo,
        zeige_feldinfo=zeige_feldinfo,
        felder_infos=felder_infos,
        konto=session.get("konto", [])
    )

@app.route("/feld_aktion", methods=["POST"])
def feld_aktion():
    data = request.get_json()
    aktion = data.get("aktion")
    feld_idx = int(data.get("feld"))
    felder_infos = lade_felder_infos()
    # Fehlerbehandlung: Index prüfen
    if feld_idx >= len(felder_infos):
        return jsonify(success=False, error="Feld existiert nicht in der Datenbank!"), 400
    feld = felder_infos[feld_idx]
    aktiver = session["aktiver"]
    spielername = session["spieler"][aktiver]
    konto = session.get("konto", [30]*len(session["spieler"]))
    positionen = session.get("positionen", [0]*len(session["spieler"]))

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="saufmonopoly"
    )
    cursor = conn.cursor()
    if aktion == "kaufen" and not feld["besitzer"]:
        # Nur erlauben, wenn Spieler auf dem Feld steht
        if positionen[aktiver] == feld_idx:
            try:
                preis = int(''.join(filter(str.isdigit, str(feld["kaufpreis"] or "0"))))
            except:
                preis = 0
            konto[aktiver] = max(0, konto[aktiver] - preis)
            session["konto"] = konto
            # Besitzer wird in der DB gespeichert:
            cursor.execute("UPDATE spielfelder SET besitzer=%s WHERE feld_id=%s", (spielername, feld["feld_id"]))
            conn.commit()
    elif aktion == "miete" and feld["besitzer"] and feld["besitzer"] != spielername:
        if positionen[aktiver] == feld_idx:
            try:
                miete = int(''.join(filter(str.isdigit, str(feld["miete"] or "0"))))
            except:
                miete = 0
            konto[aktiver] = max(0, konto[aktiver] - miete)
            besitzer_idx = session["spieler"].index(feld["besitzer"])
            konto[besitzer_idx] += miete
            session["konto"] = konto
    cursor.close()
    conn.close()
    return jsonify(success=True)

if __name__ == "__main__":
    print("🟢 Spiel gestartet auf Feld 0")
    app.run(debug=True)