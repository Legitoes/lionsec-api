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


@app.route("/health", methods=["GET"])
def health():
    return {"v": "1.0.7"}, 200


@app.route("/api/v2/logs", methods=["GET", "POST"])
def logs_both():
    if request.method == "GET":
        return jsonify(read_logs())
    
    # Get JSON body reliably
    try:
        body = request.get_json(force=True)
    except:
        try:
            body = json.loads(request.data.decode("utf-8"))
        except:
            body = {}

    # ✅ ONLY use URL params for UPDATE
    log_id_url = request.args.get("id")
    status_url = request.args.get("status")

    # ✅ UPDATE: ONLY if BOTH id AND status are in the URL
    if log_id_url and status_url:
        logs = read_logs()
        for log in logs:
            if str(log.get("log_id","")).strip().upper() == str(log_id_url).strip().upper():
                log["status"] = status_url
                save_logs(logs)
                return jsonify({"success": True}), 200
        return jsonify({"error": "Not found"}), 404

    # ✅ CREATE: always reached from bot!
    else:
        if not body or "log_id" not in body:
            return jsonify({"error": "Missing log_id"}), 400
        if "status" not in body or not body["status"]:
            body["status"] = "In place"
        logs = read_logs()
        logs.insert(0, body)
        save_logs(logs)
        return jsonify({"success": True}), 201


@app.route("/api/v2/clear", methods=["GET", "POST"])
def clear():
    save_logs([])
    return jsonify({"cleared": True}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
