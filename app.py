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

# ✅ HEALTH ROUTE — KEEPS YOUR API AWAKE
@app.route("/health", methods=["GET"])
def health():
    return {"status": "awake"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
# ---------------- ADD THIS TO YOUR API ----------------
@app.route("/api/logs/clear-lionsec", methods=["POST"])
def clear_logs_lionsec():
    # THIS CLEARS ALL LOGS — KEEP THIS SECURE!
    import json
    try:
        with open("logs.json", "w") as f:
            json.dump([], f)  # EMPTY THE FILE
        return jsonify({"success": True, "message": "ALL LOGS CLEARED"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
# -------------------------------------------------------
