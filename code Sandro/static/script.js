function wuerfeln() {
    const btn = document.getElementById('wuerfelnBtn');
    if (btn) btn.disabled = true;

    // Animation: 13x zufällig wechseln (1 Sekunde bei 80ms)
    let count = 0;
    const max = 13;
    const w1 = document.getElementById('w1');
    const w2 = document.getElementById('w2');
    const anzeige = document.getElementById('anzeige');

    anzeige.textContent = "";

    const anim = setInterval(() => {
        w1.src = `/static/dice/${Math.floor(Math.random()*6)+1}.png`;
        w2.src = `/static/dice/${Math.floor(Math.random()*6)+1}.png`;
        count++;
        if (count >= max) {
            clearInterval(anim);
            // Nach der Animation Formular absenden (echter Wurf und Bewegung vom Server)
            const form = btn.closest('form');
            if (form) form.submit();
        }
    }, 80);
    return false; // Verhindert sofortiges Absenden
}

window.addEventListener("DOMContentLoaded", function() {
    // Wenn ein Wurf vom Server kommt, zeige die richtigen Würfelbilder an
    if (window.wurf && Array.isArray(window.wurf)) {
        const w1 = document.getElementById('w1');
        const w2 = document.getElementById('w2');
        if (w1 && w2) {
            w1.src = `/static/dice/${window.wurf[0]}.png`;
            w2.src = `/static/dice/${window.wurf[1]}.png`;
        }
    }

    // Spielfeld-Felder klickbar machen
    document.querySelectorAll('.feld[data-feld-index]').forEach(function(feldDiv) {
        feldDiv.addEventListener('click', function(e) {
            const idx = parseInt(feldDiv.getAttribute('data-feld-index'));
            const feld = window.felder_infos && window.felder_infos[idx];
            if (!feld) return;
            let html = `<h3>${feld.name}</h3>`;
            html += `<p>Typ: <b>${feld.typ}</b></p>`;
            if (feld.kaufpreis) html += `<p>Kaufpreis: <b>${feld.kaufpreis}</b></p>`;
            if (feld.miete) html += `<p>Miete: <b>${feld.miete}</b></p>`;
            if (feld.farbe) html += `<p>Farbe: <b>${feld.farbe}</b></p>`;
            html += `<p>Alkohol: <b>${feld.alkohol_typ}</b> (${feld.alkohol_menge})</p>`;
            if (feld.zusatz_regel) html += `<p>Regel: <b>${feld.zusatz_regel}</b></p>`;
            // Nur wenn aktiver Spieler auf diesem Feld steht, Button anzeigen
            const aktiverIndex = window.aktiverIndex;
            const aktPos = Array.isArray(window.positionen) ? window.positionen[aktiverIndex] : null;
            if (!feld.besitzer) {
                html += `<p>Dieses Feld ist frei.</p>`;
                if (aktPos === idx) {
                    html += `<button id="kaufen-btn" data-feld="${idx}">Feld kaufen</button>`;
                }
            } else if (feld.besitzer !== window.aktiverSpieler) {
                html += `<p>Besitzer: <b>${feld.besitzer}</b></p>`;
                if (aktPos === idx) {
                    html += `<button id="miete-btn" data-feld="${idx}">Miete zahlen</button>`;
                }
            } else {
                html += `<p>Du besitzt dieses Feld.</p>`;
            }
            document.getElementById('feld-modal-content').innerHTML = html;
            document.getElementById('feld-modal').style.display = 'block';

            // Kaufen-Button Event
            setTimeout(() => {
                const kaufenBtn = document.getElementById('kaufen-btn');
                if (kaufenBtn) {
                    kaufenBtn.onclick = function() {
                        fetch('/feld_aktion', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({aktion: 'kaufen', feld: kaufenBtn.getAttribute('data-feld')})
                        }).then(res => res.json()).then(() => {
                            // Modal schließen nach Kauf
                            document.getElementById('feld-modal').style.display = 'none';
                        });
                    };
                }
                const mieteBtn = document.getElementById('miete-btn');
                if (mieteBtn) {
                    mieteBtn.onclick = function() {
                        fetch('/feld_aktion', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({aktion: 'miete', feld: mieteBtn.getAttribute('data-feld')})
                        }).then(res => res.json()).then(() => {
                            document.getElementById('feld-modal').style.display = 'none';
                        });
                    };
                }
            }, 100);
        });
    });
});
