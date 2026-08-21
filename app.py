from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

logs = []

@app.route("/api/logs", methods=["GET"])
def get_logs():
    return jsonify(logs)

@app.route("/api/logs", methods=["POST"])
def add_log():
    data = request.json
    logs.insert(0, data)
    print(f"📥 Log received: {data}")
    return jsonify({"status": "ok"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
@app.route("/health", methods=["GET"])
def health():
    return {"status": "awake"}
