from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/stock/<sku>', methods=['GET'])
def get_stock(sku):
    # Service rapide et fiable
    return jsonify({"sku": sku, "stock": 42, "status": "AVAILABLE"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
    