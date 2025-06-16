from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

FELD_ANZAHL = 40

def reset_besitzer():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="saufmonopoly"
    )
    cursor = conn.cursor()
    cursor.execute("UPDATE spielfelder SET besitzer=NULL")
    conn.commit()
    cursor.close()
    conn.close()

def lade_felder_infos():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="saufmonopoly"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM spielfelder ORDER BY feld_id ASC")
    felder_infos = cursor.fetchall()
    cursor.close()
    conn.close()
    return felder_infos

def get_besitz_uebersicht():
    felder_infos = lade_felder_infos()
    besitz = {}
    for feld in felder_infos:
        if feld.get("besitzer"):
            besitz.setdefault(feld["besitzer"], []).append(feld)
    return besitz

def parse_schlucke(text):
    import re
    if not text:
        return 0
    match = re.search(r"(\d+)", str(text))
    return int(match.group(1)) if match else 0

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session.clear()
        anzahl = int(request.form["anzahl"])
        session["anzahl"] = anzahl
        return redirect(url_for("namen"))
    return render_template("index.html")

@app.route("/namen", methods=["GET", "POST"])
def namen():
    if request.method == "POST":
        spieler = []
        for i in range(1, session["anzahl"] + 1):
            spieler.append(request.form[f"spieler{i}"])
        session["spieler"] = spieler
        session["positionen"] = [0 for _ in range(len(spieler))]
        session["aktiver"] = 0
        session["konto"] = [0] * len(spieler)
        session["gesamt"] = [0] * len(spieler)
        session["pending_popup"] = None
        session["warte_auf_wurf"] = True
        return redirect(url_for("spiel"))
    return render_template("spielernamen.html", anzahl=session["anzahl"])

@app.route("/board", methods=["GET", "POST"])
def spiel():
    felder_infos = lade_felder_infos()
    aktiver = session.get("aktiver", 0)
    pos_liste = session.get("positionen", [])
    pending_popup = session.get("pending_popup")
    warte_auf_wurf = session.get("warte_auf_wurf", True)
    wurf = session.get("wurf")

    # 1. Spieler ist dran
    if warte_auf_wurf:
        if request.method == "POST":
            # Würfeln im Backend!
            würfel1 = random.randint(1, 6)
            würfel2 = random.randint(1, 6)
            summe = würfel1 + würfel2
            session["wurf"] = [würfel1, würfel2]
            session["warte_auf_wurf"] = False
            return redirect("/board")
        return render_template(
            "board.html",
            spieler=session.get("spieler", []),
            aktiver=aktiver,
            zeige_wer_ist_dran=True,
            felder_infos=felder_infos,
            positionen=pos_liste,
            konto=session.get("konto", []),
            besitz=get_besitz_uebersicht(),
            felder=list(range(40)),
            wurf=None,
            feldinfo=None,
            popup_spieler=None,
            zeige_feldinfo=False,
            zeige_wurf_popup=False
        )

    # 2. Würfelanimation und Wurf-Popup
    if not warte_auf_wurf and not pending_popup:
        if request.method == "POST":
            wurf = session.get("wurf")
            summe = wurf[0] + wurf[1]
            aktuelle_pos = session["positionen"][aktiver]
            neue_pos = (aktuelle_pos + summe) % len(felder_infos)
            session["positionen"][aktiver] = neue_pos
            session["gesamt"][aktiver] += summe
            session["pending_popup"] = {
                "spieler": aktiver,
                "feld": neue_pos,
                "wurf": wurf
            }
            session["wurf"] = None
            session["warte_auf_wurf"] = False
            return redirect("/board")
        return render_template(
            "board.html",
            spieler=session.get("spieler", []),
            aktiver=aktiver,
            zeige_wer_ist_dran=False,
            felder_infos=felder_infos,
            positionen=session.get("positionen", []),
            konto=session.get("konto", []),
            besitz=get_besitz_uebersicht(),
            felder=list(range(40)),
            wurf=session.get("wurf"),
            feldinfo=None,
            popup_spieler=None,
            zeige_feldinfo=False,
            zeige_wurf_popup=True
        )

    # 3. Feld-Popup
    if pending_popup:
        popup_spieler = pending_popup["spieler"]
        popup_feldinfo = felder_infos[pending_popup["feld"]]
        popup_wurf = pending_popup["wurf"]
    else:
        popup_feldinfo = None
        popup_spieler = None
        popup_wurf = None

    return render_template(
        "board.html",
        felder=list(range(40)),  # <-- KORREKT: Board-Index 0..39
        spieler=session.get("spieler", []),
        positionen=session.get("positionen", []),
        aktiver=aktiver,
        wurf=popup_wurf,
        feldinfo=popup_feldinfo,
        popup_spieler=popup_spieler,
        zeige_feldinfo=bool(pending_popup),
        felder_infos=felder_infos,
        konto=session.get("konto", []),
        besitz=get_besitz_uebersicht(),
        zeige_wer_ist_dran=False,
        zeige_wurf_popup=False
    )

@app.route("/feld_aktion", methods=["POST"])
def feld_aktion():
    data = request.get_json()
    aktion = data.get("aktion")
    board_index = int(data.get("feld"))  # Das ist der Index 0..39
    pending_popup = session.get("pending_popup")
    if not pending_popup:
        return jsonify({"ok": False, "msg": "Kein aktiver Zug!"})

    aktiver = pending_popup["spieler"]
    felder_infos = lade_felder_infos()
    feld = felder_infos[board_index]
    feld_id = feld["feld_id"]

    if aktion == "kaufen":
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="saufmonopoly"
        )
        cursor = conn.cursor()
        spielername = session["spieler"][aktiver]
        cursor.execute("UPDATE spielfelder SET besitzer=%s WHERE feld_id=%s", (spielername, feld_id))
        conn.commit()
        cursor.close()
        conn.close()
        schlucke = parse_schlucke(feld.get("kaufpreis"))
        session["konto"][aktiver] += schlucke
        session["pending_popup"] = None
        session["aktiver"] = (aktiver + 1) % len(session["spieler"])
        session["warte_auf_wurf"] = True
        return jsonify({"ok": True})

    if aktion == "miete":
        besitzer_name = feld.get("besitzer")
        if besitzer_name:
            schlucke = parse_schlucke(feld.get("miete"))
            session["konto"][aktiver] += schlucke
        session["pending_popup"] = None
        session["aktiver"] = (aktiver + 1) % len(session["spieler"])
        session["warte_auf_wurf"] = True
        return jsonify({"ok": True})

    if aktion == "skip":
        session["pending_popup"] = None
        session["aktiver"] = (aktiver + 1) % len(session["spieler"])
        session["warte_auf_wurf"] = True
        return jsonify({"ok": True})

    return jsonify({"ok": False})

if __name__ == "__main__":
    reset_besitzer()
    app.run(debug=True)