import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# جلب توكن البوت والـ Chat ID من متغيرة البيئة أو كتابتهما مباشرة
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8572152998:AAFM2pXz84AUQTqUiwGqQDfvRg315ROWZOo")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "8572152998")

@app.route('/webhook', methods=['POST'])
def webhook():
    # استقبال نص التنبيه المرسل من TradingView
    alert_text = request.get_data(as_text=True)
    
    if not alert_text:
        return jsonify({"status": "error", "message": "No data received"}), 400

    # إرسال النص مباشرة إلى بوت تيليجرام
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": alert_text,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(telegram_url, json=payload)
        res_data = response.json()
        
        if res_data.get("ok"):
            return jsonify({"status": "success", "message": "Alert sent to Telegram"}), 200
        else:
            return jsonify({"status": "error", "details": res_data}), 400
            
    except Exception as e:
        return jsonify({"status": "error", "exception": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
