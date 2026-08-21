from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# ✅ SAVE LOGS TO FILE — PERSISTS FOREVER!
LOGS_FILE = "logs.json"

# Helper: Read logs from file
def read_logs():
    try:
        with open(LOGS_FILE, "r") as f:
            return json.load(f)
    except:
        return []  # Return empty if file missing

# Helper: Save logs to file
def save_logs(logs):
    with open(LOGS_FILE, "w") as f:
        json.dump(logs, f, indent=2)


# ✅ GET ALL LOGS
@app.route("/api/logs", methods=["GET"])
def get_logs():
    return jsonify(read_logs())


# ✅ CREATE NEW LOG + UPDATE STATUS — ALL IN ONE!
@app.route("/api/logs", methods=["POST"])
def logs_route():
    log_id_param = request.args.get("id") or request.json.get("log_id")
    new_status = request.args.get("status") or request.json.get("status")
    logs = read_logs()

    # CASE 1: UPDATE existing log status
    if log_id_param and new_status:
        found = False
        for log in logs:
            if log.get("log_id", "").upper() == log_id_param.upper():
                log["status"] = new_status
                found = True
                break
        if found:
            save_logs(logs)
            print(f"✅ UPDATED {log_id_param} → {new_status}")
            return jsonify({"success": True, "new_status": new_status}), 200
        else:
            return jsonify({"error": "Log not found"}), 404

    # CASE 2: CREATE new log
    else:
        new_log = request.get_json()
        logs.insert(0, new_log)  # New logs at top
        save_logs(logs)
        print(f"✅ NEW LOG: {new_log.get('log_id')} | Status: {new_log.get('status')}")
        return jsonify({"success": True}), 201


# ✅ CLEAR ALL LOGS
@app.route("/api/logs/clear-lionsec", methods=["POST"])
def clear_logs_lionsec():
    try:
        save_logs([])
        print("⚠️ ALL LOGS CLEARED")
        return jsonify({"success": True, "message": "ALL LOGS CLEARED"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ✅ HEALTH CHECK
@app.route("/health", methods=["GET"])
def health():
    return {"status": "awake"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
