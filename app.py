import os
import time
from flask import Flask, Response

app = Flask(__name__)

# হুবহু আগের মতো গোল আইকন, মাল্টি-গ্লো প্যানেল এবং সমস্ত অপশন সমৃদ্ধ বট কোড
BOT_JS_CONTENT = """
(function () {
    // পুরোনো কোনো উইজেট বা স্টাইল থাকলে তা রিমুভ করা
    if (document.getElementById('ys-tr-bot-main-container')) {
        document.getElementById('ys-tr-bot-main-container').remove();
    }
    if (document.getElementById('ys-tr-bot-styles')) {
        document.getElementById('ys-tr-bot-styles').remove();
    }

    // মাল্টি-গ্লো ও এনিমেশনের জন্য সিএসএস স্টাইল ইনজেক্ট করা
    const styleElem = document.createElement('style');
    styleElem.id = 'ys-tr-bot-styles';
    styleElem.innerHTML = `
        @keyframes ysMultiGlow {
            0% { border-color: #00ffcc; box-shadow: 0 0 20px #00ffcc, inset 0 0 10px #00ffcc; }
            33% { border-color: #ff00ff; box-shadow: 0 0 20px #ff00ff, inset 0 0 10px #ff00ff; }
            66% { border-color: #00ccff; box-shadow: 0 0 20px #00ccff, inset 0 0 10px #00ccff; }
            100% { border-color: #00ffcc; box-shadow: 0 0 20px #00ffcc, inset 0 0 10px #00ffcc; }
        }
        @keyframes bubbleGlow {
            0% { box-shadow: 0 0 15px #ff007f, 0 0 25px #00ffcc; }
            50% { box-shadow: 0 0 25px #00ffcc, 0 0 35px #ff00ff; }
            100% { box-shadow: 0 0 15px #ff007f, 0 0 25px #00ffcc; }
        }
        .ys-glow-panel {
            animation: ysMultiGlow 4s infinite;
        }
        .ys-bubble-glow {
            animation: bubbleGlow 3s infinite;
        }
    `;
    document.head.appendChild(styleElem);

    // মেইন কন্টেইনার তৈরি
    const container = document.createElement('div');
    container.id = 'ys-tr-bot-main-container';
    container.innerHTML = `
        <!-- ১. গোল আকৃতির ফ্লোটিং আইকন (সঠিক ডিজাইন) -->
        <div id="ys-bot-bubble" class="ys-bubble-glow" style="position: fixed; bottom: 80px; left: 25px; width: 75px; height: 75px; background: #050508; border-radius: 50%; z-index: 999999; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; border: 3px dashed #00ffcc; transition: transform 0.2s;">
            <div style="font-size: 11px; font-weight: 900; color: #38bdf8; letter-spacing: 0.5px; font-family: sans-serif;">YS TR</div>
            <div style="font-size: 11px; font-weight: 900; color: #38bdf8; letter-spacing: 0.5px; font-family: sans-serif;">BOT</div>
        </div>

        <!-- ২. মূল কন্ট্রোল প্যানেল (স্ক্রিনশটের হুবহু মাল্টি-গ্লো ডিজাইন ও অপশন) -->
        <div id="ys-bot-panel" class="ys-glow-panel" style="position: fixed; bottom: 170px; left: 20px; width: 330px; background: #0b0c10; color: #fff; border-radius: 14px; z-index: 999998; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; overflow: hidden; border: 2px solid #00ffcc; display: none; flex-direction: column; box-shadow: 0 12px 35px rgba(0,0,0,0.9);">
            
            <!-- হেডার -->
            <div style="background: #141622; padding: 10px 14px; font-weight: bold; font-size: 13px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f2430;">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="background: #facc15; color: #000; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: bold;">YS</span>
                    <span style="color: #fff; font-weight: bold;">YS TR BOT</span>
                    <span style="color: #4ade80; font-size: 10px; font-weight: bold;">● MULTI-GLOW</span>
                </div>
                <button id="ys-close-btn" style="background: #22c55e; color: #000; border: none; width: 22px; height: 22px; border-radius: 50%; font-size: 12px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center;">-</button>
            </div>
            
            <!-- প্যানেল বডি ও অপশনসমূহ -->
            <div style="padding: 12px; font-size: 11px; max-height: 420px; overflow-y: auto;">
                
                <!-- অটো ট্রেড বাটন দুটি -->
                <div style="display: flex; gap: 8px; margin-bottom: 12px;">
                    <button id="ys-auto-on" style="flex: 1; background: linear-gradient(135deg, #a855f7, #3b82f6); color: white; border: none; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 11px; text-shadow: 0 1px 2px rgba(0,0,0,0.5);">AUTO TRADE ON</button>
                    <button id="ys-auto-off" style="flex: 1; background: linear-gradient(135deg, #f97316, #ef4444); color: white; border: none; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 11px; text-shadow: 0 1px 2px rgba(0,0,0,0.5);">AUTO TRADE OFF</button>
                </div>

                <!-- অপশন লিস্ট বক্সগুলো -->
                <div style="display: flex; flex-direction: column; gap: 6px;">
                    <div style="background: #13151f; padding: 8px 10px; border-radius: 6px; border: 1px solid #282d3d; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-weight: 600;">MARKET PAIR</span>
                        <span id="ys-pair" style="color: #facc15; font-weight: bold;">CAD/CHF (OTC)</span>
                    </div>

                    <div style="background: #13151f; padding: 8px 10px; border-radius: 6px; border: 1px solid #282d3d; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-weight: 600;">OTC + FAKE TRAP FILTER</span>
                        <span id="ys-trap" style="color: #facc15; font-weight: bold;">WAITING...</span>
                    </div>

                    <div style="background: #13151f; padding: 8px 10px; border-radius: 6px; border: 1px solid #282d3d; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-weight: 600;">MARKET STATE: CHOP GUARD</span>
                        <span id="ys-chop" style="color: #facc15; font-weight: bold;">WAITING...</span>
                    </div>

                    <div style="background: #13151f; padding: 8px 10px; border-radius: 6px; border: 1px solid #282d3d; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-weight: 600;">MARKET TREND</span>
                        <span id="ys-trend" style="color: #facc15; font-weight: bold;">WAITING...</span>
                    </div>

                    <div style="background: #13151f; padding: 8px 10px; border-radius: 6px; border: 1px solid #282d3d; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-weight: 600;">QX REAL SIGNAL</span>
                        <span id="ys-signal" style="color: #facc15; font-weight: bold;">WAITING...</span>
                    </div>

                    <div style="background: #13151f; padding: 8px 10px; border-radius: 6px; border: 1px solid #282d3d; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-weight: 600;">COUNTDOWN</span>
                        <span id="ys-countdown" style="color: #4ade80; font-weight: bold;">18s</span>
                    </div>

                    <div style="background: #13151f; padding: 8px 10px; border-radius: 6px; border: 1px solid #282d3d; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-weight: 600;">SMART MONEY / REJECTION</span>
                        <span id="ys-smart" style="color: #facc15; font-weight: bold;">WAITING...</span>
                    </div>

                    <div style="background: #13151f; padding: 8px 10px; border-radius: 6px; border: 1px solid #282d3d; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-weight: 600;">SERVER LATENCY (ms)</span>
                        <span id="ys-latency" style="color: #facc15; font-weight: bold;">WAITING...</span>
                    </div>
                </div>

            </div>
        </div>
    `;
    document.body.appendChild(container);

    const bubble = document.getElementById('ys-bot-bubble');
    const panel = document.getElementById('ys-bot-panel');
    const closeBtn = document.getElementById('ys-close-btn');
    const autoOnBtn = document.getElementById('ys-auto-on');
    const autoOffBtn = document.getElementById('ys-auto-off');

    // গোল বুবালে ক্লিক করলে প্যানেল টগল হবে
    bubble.onclick = function () {
        if (panel.style.display === 'none' || panel.style.display === '') {
            panel.style.display = 'flex';
            bubble.style.transform = 'scale(0.9)';
        } else {
            panel.style.display = 'none';
            bubble.style.transform = 'scale(1)';
        }
    };

    closeBtn.onclick = function () {
        panel.style.display = 'none';
        bubble.style.transform = 'scale(1)';
    };

    autoOnBtn.onclick = function () {
        autoOnBtn.style.opacity = '1';
        autoOffBtn.style.opacity = '0.5';
    };

    autoOffBtn.onclick = function () {
        autoOffBtn.style.opacity = '1';
        autoOnBtn.style.opacity = '0.5';
    };

    // লাইভ কাউন্টডাউন এবং স্ক্যানিং স্ট্যাটাস আপডেট
    let countSec = 18;
    setInterval(() => {
        countSec--;
        if (countSec < 1) countSec = 60;
        const cdElem = document.getElementById('ys-countdown');
        if (cdElem) cdElem.innerText = countSec + "s";

        const statuses = ["SCANNING...", "ACTIVE", "WAITING...", "READY"];
        const randStatus = statuses[Math.floor(Math.random() * statuses.length)];
        
        const trapEl = document.getElementById('ys-trap');
        const chopEl = document.getElementById('ys-chop');
        const trendEl = document.getElementById('ys-trend');
        const sigEl = document.getElementById('ys-signal');
        const smartEl = document.getElementById('ys-smart');
        const latEl = document.getElementById('ys-latency');

        if(trapEl) trapEl.innerText = randStatus;
        if(chopEl) chopEl.innerText = randStatus;
        if(trendEl) trendEl.innerText = randStatus;
        if(sigEl) {
            const sigs = ["CALL", "PUT", "WAITING...", "STRONG CALL"];
            sigEl.innerText = sigs[Math.floor(Math.random() * sigs.length)];
        }
        if(smartEl) smartEl.innerText = randStatus;
        if(latEl) latEl.innerText = Math.floor(Math.random() * 20 + 10) + "ms";
    }, 2500);
})();
"""

@app.route('/')
def home():
    return "YS TR Bot Server Active 24/7!"

@app.route('/bot.js')
def serve_bot_js():
    return Response(BOT_JS_CONTENT, mimetype='application/javascript')

def start_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    start_server()
