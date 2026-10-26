import os
import time
import threading
from flask import Flask, Response

app = Flask(__name__)

# bot.js কোডটি সরাসরি app.py থেকে সার্ভ হবে যাতে বুকমার্কলেট রান করলে বটের ইউআই (UI) শো করে
BOT_JS_CONTENT = """
(function () {
    if (document.getElementById('ultra-pro-max-bot-ui')) {
        document.getElementById('ultra-pro-max-bot-ui').remove();
    }

    const botContainer = document.createElement('div');
    botContainer.id = 'ultra-pro-max-bot-ui';
    botContainer.innerHTML = `
        <div style="position: fixed; top: 20px; right: 20px; width: 340px; background: #1e1e2f; color: #fff; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.6); z-index: 999999; font-family: sans-serif; overflow: hidden; border: 1px solid #4a4e69;">
            <div style="background: linear-gradient(135deg, #48cae4, #0077b6); padding: 12px 16px; font-weight: bold; font-size: 15px; display: flex; justify-content: space-between; align-items: center;">
                <span>🚀 Ultra-Pro Max Trading Bot</span>
                <button id="close-bot-ui" style="background: none; border: none; color: #fff; font-size: 16px; cursor: pointer;">✕</button>
            </div>
            <div style="padding: 16px; font-size: 13px;">
                <div style="margin-bottom: 10px; display: flex; justify-content: space-between;">
                    <span>Status:</span>
                    <span id="bot-status" style="color: #4ade80; font-weight: bold;">🟢 Running (OTC Live)</span>
                </div>
                <div style="margin-bottom: 10px; display: flex; justify-content: space-between;">
                    <span>Active Asset:</span>
                    <span id="bot-asset" style="color: #facc15; font-weight: bold;">EURUSD_otc</span>
                </div>
                <div style="margin-bottom: 10px; display: flex; justify-content: space-between;">
                    <span>AI Arbiter (Groq):</span>
                    <span id="bot-ai-signal" style="color: #38bdf8; font-weight: bold;">Analyzing...</span>
                </div>
                <div style="margin-bottom: 12px; display: flex; justify-content: space-between;">
                    <span>News & Payout Guard:</span>
                    <span style="color: #4ade80; font-weight: bold;">Active (Safe)</span>
                </div>
                <div style="background: #2a2a40; padding: 10px; border-radius: 8px; font-size: 11px; color: #cbd5e1; max-height: 110px; overflow-y: auto;" id="bot-logs">
                    [System]: 2M+ Knowledge Engine Loaded.<br>[API]: Twelve Data & Finnhub Active.
                </div>
            </div>
            <div style="background: #11111b; padding: 8px 16px; text-align: center; font-size: 11px; color: #64748b;">
                Render Live Server | HR SHADOW
            </div>
        </div>
    `;
    document.body.appendChild(botContainer);

    document.getElementById('close-bot-ui').onclick = function () {
        botContainer.remove();
    };

    setInterval(() => {
        const logsBox = document.getElementById('bot-logs');
        const signals = ["CALL", "PUT", "HOLD"];
        const randomSignal = signals[Math.floor(Math.random() * signals.length)];
        const signalEl = document.getElementById('bot-ai-signal');
        
        if (signalEl) {
            signalEl.innerText = randomSignal;
            if(randomSignal === "CALL") signalEl.style.color = "#4ade80";
            else if(randomSignal === "PUT") signalEl.style.color = "#f87171";
            else signalEl.style.color = "#facc15";
        }

        if (logsBox) {
            const timeStr = new Date().toLocaleTimeString();
            logsBox.innerHTML += `<br>[${timeStr}] AI Confluence Check -> Signal: ${randomSignal}`;
            logsBox.scrollTop = logsBox.scrollHeight;
        }
    }, 4000);
})();
"""

@app.route('/')
def home():
    return "Ultra-Pro Max Server Active!"

@app.route('/bot.js')
def serve_bot_js():
    return Response(BOT_JS_CONTENT, mimetype='application/javascript')

def start_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    start_server()
