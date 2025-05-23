import os
import requests
import base64
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VT_API_KEY")
HEADERS = {"x-apikey": API_KEY}
VT_URL = "https://www.virustotal.com/api/v3/urls"

def analyse_virustotal(url: str) -> dict:
    if not API_KEY:
        return {"erreur": "Clé API VirusTotal manquante"}

    try:
        # Étape 1 : encoder l’URL
        encoded_url = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

        # Étape 2 : requête GET sur l'URL encodée
        resp = requests.get(f"{VT_URL}/{encoded_url}", headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()["data"]

        # Résultats
        stats = data["attributes"]["last_analysis_stats"]
        detections = data["attributes"]["last_analysis_results"]

        menaces = {
            engine: info["result"]
            for engine, info in detections.items()
            if info["category"] in ("malicious", "phishing", "suspicious")
        }

        niveau = "élevé" if stats["malicious"] > 5 else "modéré" if stats["malicious"] > 0 else "faible"

        return {
            "domaine": urlparse(url).netloc,
            "niveau_risque": niveau,
            "moteurs_detecteurs": list(menaces.keys()),
            "detections": stats["malicious"],
            "resume": menaces
        }

    except Exception as e:
        return {"erreur": str(e)}

