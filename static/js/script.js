document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("analyseForm");
  const resultat = document.getElementById("resultat");
  const alerterBtn = document.getElementById("alerterBtn");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const numero = form.numero.value;
    const texte = form.texte.value;

    resultat.innerHTML = "<p>Analyse en cours...</p>";
    resultat.style.display = "block";

    try {
      const res = await fetch("/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ numero, texte })
      });

      const data = await res.json();

      // Construction du résultat lisible
      const message = `
        🧾 Résumé de l’analyse :
        -----------------------------------
        📞 Numéro : ${data.numero}
        🌍 Pays : ${data.phoneinfoga?.pays || 'N/A'}
        ⚠️ Suspect : ${data.phoneinfoga?.indications_fraude ? 'Oui' : 'Non'}
        🕵️ Sources : ${data.phoneinfoga?.sources_detectées?.join(', ') || 'Aucune'}

        🔗 URL détectée : ${data.url || 'Aucune'}
        ☣️ Risque VirusTotal : ${data.virustotal?.niveau_risque || 'Non analysé'}
        ⚠️ Détections : ${data.virustotal?.detections || 0}
        🔍 Moteurs : ${data.virustotal?.moteurs_detecteurs?.join(', ') || 'Aucun'}
      `;

      resultat.innerHTML = `<pre>${message}</pre>`;

      // Stocker les données pour l'alerte
      alerterBtn.dataset.message = message;

    } catch (error) {
      resultat.innerHTML = `<p style="color:red;">Erreur lors de l’analyse.</p>`;
    }
  });

  alerterBtn.addEventListener("click", () => {
    const message = alerterBtn.dataset.message || "Aucune analyse disponible.";
    const subject = encodeURIComponent("Signalement de phishing via PhishGuard");
    const body = encodeURIComponent(`Bonjour,\n\nJe souhaite signaler un cas de phishing détecté via PhishGuard :\n\n${message}\n\nCordialement,\n[Votre nom]`);
    const mailtoLink = `mailto:cert-fr@ssi.gouv.fr?subject=${subject}&body=${body}`;
    window.location.href = mailtoLink;
  });
});


