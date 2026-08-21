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


# ✅ MUST HAVE THIS EXACT ROUTE
@app.route("/api/logs", methods=["GET"])
def get_logs():
    return jsonify(read_logs())


# ✅ MUST HAVE THIS EXACT ROUTE
@app.route("/api/logs", methods=["POST"])
def logs_post():
    body = request.get_json(silent=True) or {}
    log_id = request.args.get("id") or body.get("log_id")
    new_status = request.args.get("status") or body.get("status")
    logs = read_logs()

    if log_id and new_status:
        for log in logs:
            if str(log.get("log_id","")).strip().upper() == str(log_id).strip().upper():
                log["status"] = new_status
                save_logs(logs)
                print(f"🔄 UPDATED {log_id} → {new_status}")
                return jsonify({"success": True}), 200
        return jsonify({"error": "Not found"}), 404
    else:
        if "status" not in body or not body["status"]:
            body["status"] = "In place"
        logs.insert(0, body)
        save_logs(logs)
        print(f"📝 CREATED: {body.get('log_id')}")
        return jsonify({"success": True}), 201


@app.route("/api/logs/clear-lionsec", methods=["GET", "POST"])
def clear():
    save_logs([])
    return jsonify({"cleared": True}), 200


@app.route("/health", methods=["GET"])
def health():
    return {"ok": True}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
