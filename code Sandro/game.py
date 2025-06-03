from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Spielerposition (Index von 0 bis 39)
player_position = 0

# Spielfeld: 11x11, nur äußere Felder im Uhrzeigersinn
felder = (
    [(x, 0) for x in range(11)] +                # Oben
    [(10, y) for y in range(1, 11)] +            # Rechts
    [(x, 10) for x in range(9, -1, -1)] +        # Unten
    [(0, y) for y in range(9, 0, -1)]            # Links
)

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
        session["gesamt"] = [0] * len(spieler)
        return redirect("/board")
    return render_template("spielernamen.html", anzahl=session["anzahl"])

@app.route("/dice")
def dice():
    spieler = session.get("spieler", [])
    aktiver = session.get("aktiver", 0)
    return render_template("board.html", spieler=spieler, aktiver=aktiver)


    

@app.route("/board", methods=["GET", "POST"])
def spiel():
    global player_position  # globale Variable verwenden
    wurf = None

    if request.method == "POST":
        würfel1 = random.randint(1, 6)
        würfel2 = random.randint(1, 6)
        summe = würfel1 + würfel2
        doppel = würfel1 == würfel2
        aktiver = session["aktiver"]
        session["gesamt"][aktiver] += summe
        if not doppel:
            session["aktiver"] = (aktiver + 1) % len(session["spieler"])
        player_position = (player_position + summe) % len(felder)
        print(f"🎲 Gewürfelt: {summe} → Neue Position: {player_position}")
        return {
            "w1": würfel1,
            "w2": würfel2,
            "summe": summe,
            "doppel": doppel,
            "spieler": session["spieler"][session["aktiver"]],
            "gesamt": session["gesamt"]
        }

    return render_template("board.html",
                           felder=felder,
                           spieler_pos=felder[player_position],
                           wurf=wurf)


   

if __name__ == "__main__":
    print("🟢 Spiel gestartet auf Feld 0")
    app.run(debug=True) 