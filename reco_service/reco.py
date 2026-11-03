import time
from flask import Flask, jsonify, request

app = Flask(__name__)

# État interne pour le chaos engineering
state = {
    "down": False,
    "latency": 2.5  # lent par défaut
}

@app.route('/reco/<sku>', methods=['GET'])
def get_reco(sku):
    if state["down"]:
        return jsonify({"error": "Service Unavailable"}), 503
    
    time.sleep(state["latency"])
    return jsonify({"sku": sku, "recommendations": ["prod_B", "prod_C"]})

@app.route('/admin', methods=['GET'])
def admin():
    down = request.args.get('down')
    latency = request.args.get('latency')
    if down is not None:
        state["down"] = (down == '1')
    if latency is not None:
        state["latency"] = float(latency)
    return jsonify(state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083)
    