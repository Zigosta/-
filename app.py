from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# 최근 신호 기록
last_signal_time = {}
MIN_INTERVAL = 60  # 초 단위, 예: 60초 안에 같은 방향 신호 무시

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    symbol = data.get("symbol")
    side = data.get("side")  # "buy" 또는 "sell"
    price = float(data.get("price", 0))

    now = time.time()
    key = f"{symbol}_{side}"

    # 1. 최근 동일 신호가 너무 빨리 들어온 경우 무시
    if key in last_signal_time and now - last_signal_time[key] < MIN_INTERVAL:
        print(f"🚫 {symbol} {side} 신호 무시 (쿨다운 {MIN_INTERVAL}초)")
        return jsonify({"status": "ignored", "reason": "cooldown"})

    # 2. (선택) 가격 변화폭 체크
    # 예: 이전 가격 대비 0.1% 미만 변화면 무시
    # if abs(price - last_price.get(symbol, 0)) / price < 0.001:
    #     return jsonify({"status": "ignored", "reason": "small price change"})

    # 신호 처리
    print(f"✅ {symbol} {side} 실행, 가격: {price}")
    last_signal_time[key] = now

    # 여기서 거래소 API 호출 로직 실행
    return jsonify({"status": "executed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)