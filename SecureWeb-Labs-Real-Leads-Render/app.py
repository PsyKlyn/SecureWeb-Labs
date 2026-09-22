import os
import re
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/assessment")
def assessment():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    website = str(data.get("website", "")).strip()
    message = str(data.get("message", "")).strip()

    if not name or not email or not website:
        return jsonify({"error": "Please complete the required fields."}), 400

    if len(name) > 120 or len(email) > 254 or len(website) > 500 or len(message) > 3000:
        return jsonify({"error": "One or more fields are too long."}), 400

    if not EMAIL_RE.match(email):
        return jsonify({"error": "Please enter a valid email address."}), 400

    if not DISCORD_WEBHOOK_URL:
        app.logger.error("DISCORD_WEBHOOK_URL is not configured.")
        return jsonify({"error": "The lead service is not configured yet."}), 503

    embed = {
        "title": "🔐 New Website Security Assessment Lead",
        "color": 17407,
        "fields": [
            {"name": "Name", "value": name[:1024], "inline": True},
            {"name": "Email", "value": email[:1024], "inline": True},
            {"name": "Website", "value": website[:1024], "inline": False},
            {"name": "Message", "value": (message or "No additional message.")[:1024], "inline": False},
        ],
        "footer": {"text": "SecureWeb Labs • Authorized assessment inquiries only"},
    }

    try:
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json={"embeds": [embed]},
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException:
        app.logger.exception("Discord webhook request failed.")
        return jsonify({"error": "We couldn't send your request right now. Please try again."}), 502

    return jsonify({"ok": True}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
