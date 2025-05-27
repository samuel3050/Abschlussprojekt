from flask import Flask, render_template, request, redirect, session, url_for
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

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
        return redirect("/dice")
    return render_template("spielernamen.html", anzahl=session["anzahl"])

@app.route("/dice")
def dice():
    spieler = session.get("spieler", [])
    aktiver = session.get("aktiver", 0)
    return render_template("dice.html", spieler=spieler, aktiver=aktiver)

@app.route("/roll")
def roll():
    würfel1 = random.randint(1, 6)
    würfel2 = random.randint(1, 6)
    summe = würfel1 + würfel2
    doppel = würfel1 == würfel2
    aktiver = session["aktiver"]
    session["gesamt"][aktiver] += summe
    if not doppel:
        session["aktiver"] = (aktiver + 1) % len(session["spieler"])
    return {
        "w1": würfel1,
        "w2": würfel2,
        "summe": summe,
        "doppel": doppel,
        "spieler": session["spieler"][session["aktiver"]],
        "gesamt": session["gesamt"]
    }

if __name__ == "__main__":
    app.run(debug=True)