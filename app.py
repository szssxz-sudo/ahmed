import os
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Use Render environment variables only
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Optional: set logging
logging.basicConfig(level=logging.INFO)

@app.route("/")
def home():
    return "ahmed is live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    # Accept JSON, raw text, or form data from TradingView
    data = request.get_json(silent=True)

    if isinstance(data, dict):
        alert_text = data.get("text") or data.get("message") or str(data)
    else:
        alert_text = request.get_data(as_text=True)

    if not alert_text:
        return jsonify({"status": "error", "message": "No data received"}), 400

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return jsonify({
            "status": "error",
            "message": "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables"
        }), 500

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": alert_text,
        "parse_mode": "HTML"
    }

    try:
        import requests
        response = requests.post(telegram_url, json=payload, timeout=15)
        response.raise_for_status()
        res_data = response.json()

        if res_data.get("ok"):
            return jsonify({"status": "success", "message": "Alert sent to Telegram"}), 200

        logging.error("Telegram API error: %s", res_data)
        return jsonify({"status": "error", "details": res_data}), 400

    except Exception as exc:
        logging.exception("Telegram send failed")
        return jsonify({"status": "error", "exception": str(exc)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
