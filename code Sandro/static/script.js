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
});
