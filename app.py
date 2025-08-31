from flask import Flask, request, jsonify
import os

app = Flask(__name__)
WEBHOOK_PASSPHRASE = os.getenv("WEBHOOK_PASSPHRASE", "change-me")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if data.get("passphrase") != WEBHOOK_PASSPHRASE:
        return jsonify({"ok": False, "error": "Unauthorized"}), 401
    print("📩 받은 데이터:", data)
    # 여기에 업비트 API 주문 로직 추가 가능
    return jsonify({"ok": True})

@app.route("/health")
def health():
    return jsonify({"status": "running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
