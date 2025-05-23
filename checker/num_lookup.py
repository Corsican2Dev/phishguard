import re

def interprete_phoneinfoga(output: str) -> dict:
    interpretation = {
        "pays": None,
        "format": {},
        "sources_detectées": [],
        "indications_fraude": False,
        "commentaire": ""
    }

    # Extraction du pays
    match_country = re.search(r"Country:\s*(.+)", output)
    if match_country:
        interpretation["pays"] = match_country.group(1).strip()

    # Extraction des formats
    formats = ["Local", "Raw local", "E164", "International"]
    for f in formats:
        match = re.search(rf"{f}:\s*(.+)", output)
        if match:
            interpretation["format"][f.lower().replace(" ", "_")] = match.group(1).strip()

    # Extraction des sources détectées
    sources_detectées = []
    if "Pastebin" in output:
        sources_detectées.append("Pastebin")
    if "facebook.com" in output:
        sources_detectées.append("Facebook")
    if "instagram.com" in output:
        sources_detectées.append("Instagram")
    if "spytox" in output:
        sources_detectées.append("Spytox")
    if "who-calledme.com" in output:
        sources_detectées.append("WhoCalledMe")

    interpretation["sources_detectées"] = sources_detectées

    # ⚠️ Nouvelle logique d'évaluation
    sources_benignes = {"Facebook", "Instagram"}
    sources_suspectes = {"Pastebin", "Spytox", "WhoCalledMe"}

    sources_detectees_set = set(sources_detectées)
    fraude = len(sources_detectees_set & sources_suspectes) >= 1

    interpretation["indications_fraude"] = fraude
    if fraude:
        interpretation["commentaire"] = "Ce numéro apparaît sur des services considérés comme suspects ou frauduleux."
    elif sources_detectees_set:
        interpretation["commentaire"] = "Ce numéro apparaît sur des plateformes publiques connues, sans indication de fraude."
    else:
        interpretation["commentaire"] = "Aucune information détectée pour ce numéro."

    return interpretation
