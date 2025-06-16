function wuerfeln() {
    const btn = document.getElementById('wuerfelnBtn');
    if (btn) btn.disabled = true;

    let count = 0;
    const max = 13;
    const w1 = document.getElementById('w1');
    const w2 = document.getElementById('w2');
    const popup = document.getElementById('wurf-popup');
    const popupText = document.getElementById('wurf-popup-text');
    const popupOk = document.getElementById('wurf-popup-ok');

    let wurf1 = 1, wurf2 = 1;
    popup.style.display = 'none';
    popupOk.style.display = 'none';

    const anim = setInterval(() => {
        wurf1 = Math.floor(Math.random()*6)+1;
        wurf2 = Math.floor(Math.random()*6)+1;
        w1.src = `/static/dice/${wurf1}.png`;
        w2.src = `/static/dice/${wurf2}.png`;
        count++;
        if (count >= max) {
            clearInterval(anim);
            // Zeige NUR das kleine Popup mit Text und OK (KEINE Würfelbilder im Popup!)
            popup.style.display = 'block';
            popupText.textContent = `${window.aktiverSpieler} hat ${wurf1 + wurf2} gewürfelt!`;
            popupOk.style.display = '';
            popupOk.onclick = function() {
                popup.style.display = 'none';
                // Sende POST an /board um den Zug abzuschließen
                const form = document.getElementById('wuerfelform');
                if (form) form.submit();
            };
        }
    }, 80);
    return false;
}

// Feld kaufen Popup: "Kaufpreis bezahlt" mit Button
window.addEventListener("DOMContentLoaded", function() {
    setTimeout(() => {
        const kaufenBtn = document.getElementById('kaufen-btn');
        if (kaufenBtn) {
            kaufenBtn.onclick = function() {
                fetch('/feld_aktion', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({aktion: 'kaufen', feld: kaufenBtn.getAttribute('data-feld')})
                }).then(res => res.json()).then(() => {
                    document.getElementById('feld-modal').innerHTML = `
                        <h3>Kaufpreis bezahlt!</h3>
                        <button id="bezahlt-btn" style="margin-top:18px;">Bezahlt</button>
                    `;
                    document.getElementById('feld-modal').style.display = 'block';
                    document.getElementById('bezahlt-btn').onclick = function() {
                        document.getElementById('feld-modal').style.display = 'none';
                        setTimeout(() => location.reload(), 200);
                    };
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
                    setTimeout(() => location.reload(), 400);
                });
            };
        }
        const skipBtn = document.getElementById('skip-btn');
        if (skipBtn) {
            skipBtn.onclick = function() {
                fetch('/feld_aktion', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({aktion: 'skip', feld: skipBtn.getAttribute('data-feld')})
                }).then(() => {
                    document.getElementById('feld-modal').style.display = 'none';
                    setTimeout(() => location.reload(), 400);
                });
            };
        }
    }, 100);
});
