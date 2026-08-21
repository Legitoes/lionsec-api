from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

LOGS_FILE = "logs.json"

def read_logs():
    try:
        with open(LOGS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_logs(logs):
    with open(LOGS_FILE, "w") as f:
        json.dump(logs, f, indent=2)


# ✅ GET ALL LOGS
@app.route("/api/logs", methods=["GET"])
def get_logs():
    return jsonify(read_logs())


# ✅ CREATE NEW LOG OR UPDATE STATUS
@app.route("/api/logs", methods=["POST"])
def handle_logs():
    data = request.get_json() or {}
    log_id = request.args.get("id") or data.get("log_id")
    new_status = request.args.get("status") or data.get("status")
    
    logs = read_logs()

    # 🔄 UPDATE existing log
    if log_id and new_status:
        for log in logs:
            if log.get("log_id", "").upper() == log_id.upper():
                log["status"] = new_status
                save_logs(logs)
                print(f"✅ UPDATED {log_id} → {new_status}")
                return jsonify({"success": True}), 200
        return jsonify({"error": "Log not found"}), 404

    # 🆕 CREATE new log
    else:
        if "status" not in data or data["status"] == "":
            data["status"] = "In place"  # ✅ FORCE DEFAULT STATUS
        
        logs.insert(0, data)
        save_logs(logs)
        print(f"✅ NEW LOG created: {data.get('log_id')} | Status: {data.get('status')}")
        return jsonify({"success": True}), 201


# 🧹 CLEAR ALL LOGS
@app.route("/api/logs/clear-lionsec", methods=["POST"])
def clear_logs():
    save_logs([])
    print("⚠️ ALL LOGS CLEARED")
    return jsonify({"success": True}), 200


# 💤 KEEP ALIVE
@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
