import os
import time
import requests
from flask import Flask, jsonify

app = Flask(__name__)

STOCK_URL = os.getenv("STOCK_URL", "http://localhost:8082")
RECO_URL = os.getenv("RECO_URL", "http://localhost:8083")

# Cache pour le Fallback résilient
cache_fallback = {}

@app.route('/page/<sku>', methods=['GET'])
def get_page(sku):
    # 1. Appel Stock (Rapide)
    try:
        stock_resp = requests.get(f"{STOCK_URL}/stock/{sku}", timeout=1.0)
        stock_data = stock_resp.json()
    except Exception:
        stock_data = {"error": "Stock indisponible"}

    # 2. Appel Reco avec Timeout et Fallback (Dégradation gracieuse)
    reco_data = None
    degrade = False
    try:
        reco_resp = requests.get(f"{RECO_URL}/reco/{sku}", timeout=0.5)
        if reco_resp.status_code == 200:
            reco_data = reco_resp.json()
            cache_fallback[sku] = reco_data # Mise en cache de la dernière valeur saine
        else:
            raise Exception("Erreur service reco")
    except Exception:
        # Fallback : Utilisation du cache si disponible
        if sku in cache_fallback:
            reco_data = cache_fallback[sku]
            degrade = True
        else:
            reco_data = {"recommendations": [], "degrade": True}
            degrade = True

    return jsonify({
        "stock": stock_data,
        "reco": reco_data,
        "degrade_mode": degrade
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    