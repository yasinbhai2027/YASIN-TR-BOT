import os
from flask import Flask, jsonify, request
import threading

app = Flask(__name__)

# বটের সর্বশেষ লাইভ সিগন্যাল স্টোরেজ
latest_signal = {"signal": "HOLD", "confidence": 0, "reason": "Initializing..."}

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "message": "Quotex Ultra-Pro Max Trading Engine Running 24/7!",
        "latest_signal": latest_signal
    })

@app.route('/update_signal', methods=['POST'])
def update_signal():
    global latest_signal
    data = request.json
    if data:
        latest_signal = data
    return jsonify({"status": "success", "updated": latest_signal})

@app.route('/get_signal', methods=['GET'])
def get_signal():
    return jsonify(latest_signal)

def run_flask():
    # রেন্ডারের ডায়নামিক পোর্ট নেওয়ার জন্য os.environ ব্যবহার করা হয়েছে
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def start_server():
    server_thread = threading.Thread(target=run_flask)
    server_thread.daemon = True
    server_thread.start()
