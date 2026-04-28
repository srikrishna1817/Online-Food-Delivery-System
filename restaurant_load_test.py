"""
Experiment 12 — Load Testing Flask App
Run: python restaurant_load_test.py
Then open JMeter and load restaurant_test.jmx
"""

from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.get_json(force=True)

    # Simulate processing delay (realistic server behaviour)
    time.sleep(0.05)

    if not data or 'items' not in data:
        return jsonify({"status": "failed", "reason": "missing items"}), 400

    if len(data['items']) > 10:
        return jsonify({"status": "failed", "reason": "too many items"}), 500

    return jsonify({"status": "success", "order_id": 101})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    print("=" * 50)
    print("  Experiment 12 — Restaurant Load Test Server")
    print("  Running on http://localhost:5001")
    print("  Endpoint: POST /place_order")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5001, debug=False)
