from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Spielerposition (Index 0–39)
player_state = {"pos": 0}

# Liste der sichtbaren Felder in der Reihenfolge im Uhrzeigersinn
felder = []

# Obere Reihe (von links nach rechts)
for x in range(11):
    felder.append((x, 0))

# Rechte Spalte (von oben nach unten, ohne Ecke doppelt)
for y in range(1, 11):
    felder.append((10, y))

# Untere Reihe (von rechts nach links, ohne Ecke doppelt)
for x in range(9, -1, -1):
    felder.append((x, 10))

# Linke Spalte (von unten nach oben, ohne Ecke doppelt)
for y in range(9, 0, -1):
    felder.append((0, y))

# Das ergibt genau 40 Felder

@app.route("/", methods=["GET", "POST"])
def spiel():
    wurf = None

    if request.method == "POST":
        wurf = random.randint(1, 6)
        player_state["pos"] = (player_state["pos"] + wurf) % len(felder)
        print(f"🎲 Gewürfelt: {wurf} → Neue Position: {player_state['pos']}")
        return redirect(url_for("spiel"))

    pos_koord = felder[player_state["pos"]]
    return render_template("board.html", felder=felder, spieler_pos=pos_koord, wurf=wurf)

if __name__ == "__main__":
    print("🟢 Spiel gestartet auf Feld 0")
    app.run(debug=True)
