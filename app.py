# Point d'entrée de l'API Flask
from flask import Flask, request, jsonify
from flask import render_template
from checker.num_lookup import interprete_phoneinfoga
from checker.url_lookup import analyse_virustotal
import random
import re
import subprocess

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def chek_number():
    data = request.get_json() # Récupère les données en json
    numero = data.get('numero') # Récupère le champ "numero"
    texte = data.get('texte') # Récupère le champ "texte"

    # Extraire les première URL
    url_match = re.search(r'(https?://[^\s]+)', texte or "")
    url = url_match.group(1) if url_match else None
    vt_result = analyse_virustotal(url) if url else None


    # Analyse PhoneInfoga (exécutable dans ./tools)
    try:
        output = subprocess.check_output([
            "tools\\phoneinfoga.exe", "scan", "-n", numero
        ], 
            stderr=subprocess.STDOUT, 
            text=True, 
            shell=True
        )
    except subprocess.CalledProcessError as e:
        output = f"Erreur lors de l'exécution de PhoneInfoga : {e.output}"

    resultat = {
        'numero': numero,
        'texte': texte,
        'url': url,
        'phoneinfoga': interprete_phoneinfoga(output),
        'virustotal': vt_result
    }

    return jsonify(resultat)


if __name__ == '__main__':
    app.run(debug=True)