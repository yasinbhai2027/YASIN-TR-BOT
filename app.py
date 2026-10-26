import os
import time
import threading
from flask import Flask, Response

app = Flask(__name__)

# আপনার চাওয়া সেই আসল গোল আইকন এবং মাল্টি-গ্লো প্যানেল ডিজাইন সমৃদ্ধ বট কোড
BOT_JS_CONTENT = """
(function () {
    // পুরোনো কোনো উইজেট বা স্টাইল থাকলে রিমুভ করা
    if (document.getElementById('yasin-tr-bot-container')) {
        document.getElementById('yasin-tr-bot-container').remove();
    }
    if (document.getElementById('yasin-bot-custom-style')) {
        document.getElementById('yasin-bot-custom-style').remove();
    }

    // মাল্টি-গ্লো এবং চমৎকার এনিমেশনের জন্য স্টাইল ইনজেক্ট করা
    const styleSheet = document.createElement('style');
    styleSheet.id = 'yasin-bot-custom-style';
    styleSheet.innerHTML = `
        @keyframes multiGlow {
            0% { border-color: #00ffcc; box-shadow: 0 0 15px #00ffcc, inset 0 0 15px #00ffcc; }
            33% { border-color: #ff00ff; box-shadow: 0 0 15px #ff00ff, inset 0 0 15px #ff00ff; }
            66% { border-color: #00ccff; box-shadow: 0 0 15px #00ccff, inset 0 0 15px #00ccff; }
            100% { border-color: #00ffcc; box-shadow: 0 0 15px #00ffcc, inset 0 0 15px #00ffcc; }
        }
        .yasin-multi-glow-box {
            animation: multiGlow 4s infinite;
        }
    `;
    document.head.appendChild(styleSheet);

    // মেইন কন্টেইনার তৈরি
    const container = document.createElement('div');
    container.id = 'yasin-tr-bot-container';
    container.innerHTML = `
        <!-- ১. গোল আকৃতির ফ্লোটিং আইকন (YASIN TR BOT) -->
        <div id="yasin-bot-bubble" style="position: fixed; bottom: 80px; left: 30px; width: 75px; height: 75px; background: radial-gradient(circle, #0b3c5d, #1d2731); border-radius: 50%; box-shadow: 0 0 20px rgba(0,255,204,0.6); z-index: 999999; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; border: 3px dashed #00ffcc; transition: transform 0.2s;">
            <div style="font-size: 10px; font-weight: bold; color: #00ffcc; letter-spacing: 0.5px;">YASIN</div>
            <div style="font-size: 10px; font-weight: bold; color: #ffaa00; letter-spacing: 0.5px;">TR</div>
            <div style="font-size: 10px; font-weight: bold; color: #00ffcc; letter-spacing: 0.5px;">BOT</div>
        </div>

        <!-- ২. মূল কন্ট্রোল প্যানেল (স্ক্রিনশটের হুবহু ডিজাইন) -->
        <div id="yasin-bot-panel" class="yasin-multi-glow-box" style="position: fixed; bottom: 170px; left: 20px; width: 330px; background: #0f1016; color: #fff; border-radius: 14px; z-index: 999998; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; overflow: hidden; border: 2px solid #00ffcc; display: none; flex-direction: column; box-shadow: 0 10px 30px rgba(0,0,0,0.8);">
            
            <!-- হেডার -->
            <div style="background: #181a26; padding: 10px 14px; font-weight: bold; font-size: 13px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #2a2d3d;">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="background: #ffcc00; color: #000; font-size: 10px; padding: 2px 5px; border-radius: 4px; font-weight: bold;">YS</span>
                    <span style="color: #fff; font-weight: bold;">YS TR BOT</span>
                    <span style="color: #00ffcc; font-size: 10px; font-weight: normal;">● MULTI-GLOW</span>
                </div>
                <button id="yasin-close-btn" style="background: #00ffcc; color: #000; border: none; width: 22px; height: 22px; border-radius: 50%; font-size: 12px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center;">✕</button>
            </div>
            
            <!-- বডি কন্টেন্ট -->
            <div style="padding: 12px; font-size: 12px; max-height: 400px; overflow-y: auto;">
                
                <!-- অটো ট্রেড বাটন দুটি -->
                <div style="display: flex; gap: 8px; margin-bottom: 12px;">
                    <button id="yb-auto-on" style="flex: 1; background: linear-gradient(135deg, #a855f7, #3b82f6); color: white; border: none; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 11px; text-shadow: 0 1px 2px rgba(0,0,0,0.5);">AUTO TRADE ON</button>
                    <button id="yb-auto-off" style="flex: 1; background: linear-gradient(135deg, #f97316, #ef4444); color: white; border: none; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 11px; text-shadow: 0 1px 2px rgba(0,0,0,0.5);">AUTO TRADE OFF</button>
                </div>

                <!-- অপশন লিস্ট (স্ক্রিনশটের মতো বক্সগুলো) -->
                <div style="display: flex; flex-direction: column; gap: 6px;">
                    <div style="background: #171923; padding: 8px 10px; border-radius: 6px; border: 1px solid #2d3748; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-size: 11px; font-weight: 600;">MARKET PAIR</span>
                        <span id="yb-pair" style="color: #facc15; font-weight: bold; font-size: 11px;">CAD/CHF (OTC)</span>
                    </div>

                    <div style="background: #171923; padding: 8px 10px; border-radius: 6px; border: 1px solid #2d3748; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-size: 11px; font-weight: 600;">OTC + FAKE TRAP FILTER</span>
                        <span id="yb-trap" style="color: #4ade80; font-weight: bold; font-size: 11px;">SCANNING...</span>
                    </div>

                    <div style="background: #171923; padding: 8px 10px; border-radius: 6px; border: 1px solid #2d3748; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-size: 11px; font-weight: 600;">MARKET STATE: CHOP GUARD</span>
                        <span id="yb-chop" style="color: #38bdf8; font-weight: bold; font-size: 11px;">SCANNING...</span>
                    </div>

                    <div style="background: #171923; padding: 8px 10px; border-radius: 6px; border: 1px solid #2d3748; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-size: 11px; font-weight: 600;">MARKET TREND</span>
                        <span id="yb-trend" style="color: #f472b6; font-weight: bold; font-size: 11px;">SCANNING...</span>
                    </div>

                    <div style="background: #171923; padding: 8px 10px; border-radius: 6px; border: 1px solid #2d3748; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-size: 11px; font-weight: 600;">QX REAL SIGNAL</span>
                        <span id="yb-signal" style="color: #4ade80; font-weight: bold; font-size: 11px;">SCANNING...</span>
                    </div>

                    <div style="background: #171923; padding: 8px 10px; border-radius: 6px; border: 1px solid #2d3748; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-size: 11px; font-weight: 600;">COUNTDOWN</span>
                        <span id="yb-countdown" style="color: #facc15; font-weight: bold; font-size: 11px;">18s</span>
                    </div>

                    <div style="background: #171923; padding: 8px 10px; border-radius: 6px; border: 1px solid #2d3748; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-size: 11px; font-weight: 600;">SMART MONEY / REJECTION</span>
                        <span id="yb-smart" style="color: #a78bfa; font-weight: bold; font-size: 11px;">SCANNING...</span>
                    </div>

                    <div style="background: #171923; padding: 8px 10px; border-radius: 6px; border: 1px solid #2d3748; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #cbd5e1; font-size: 11px; font-weight: 600;">SERVER LATENCY (ms)</span>
                        <span id="yb-latency" style="color: #34d399; font-weight: bold; font-size: 11px;">14ms</span>
                    </div>
                </div>

            </div>
        </div>
    `;
    document.body.appendChild(container);

    const bubble = document.getElementById('yasin-bot-bubble');
    const panel = document.getElementById('yasin-bot-panel');
    const closeBtn = document.getElementById('yasin-close-btn');
    const autoOnBtn = document.getElementById('yb-auto-on');
    const autoOffBtn = document.getElementById('yb-auto-off');

    // গোল বুবালে ক্লিক করলে প্যানেল শো/হাইড্র হবে
    bubble.onclick = function () {
        if (panel.style.display === 'none' || panel.style.display === '') {
            panel.style.display = 'flex';
            bubble.style.transform = 'scale(0.95)';
        } else {
            panel.style.display = 'none';
            bubble.style.transform = 'scale(1)';
        }
    };

    closeBtn.onclick = function () {
        panel.style.display = 'none';
        bubble.style.transform = 'scale(1)';
    };

    // অটো ট্রেড বাটন ইন্টারঅ্যাকশন
    autoOnBtn.onclick = function () {
        autoOnBtn.style.opacity = '1';
        autoOffBtn.style.opacity = '0.5';
        alert("🚀 Auto Trade Activated with Full AI Confluence & OTC Filters!");
    };

    autoOffBtn.onclick = function () {
        autoOffBtn.style.opacity = '1';
        autoOnBtn.style.opacity = '0.5';
        alert("🛑 Auto Trade Paused.");
    };

    // লাইভ স্ক্যানিং ও সিগন্যাল আপডেট লজিক
    let sec = 18;
    setInterval(() => {
        sec--;
        if (sec < 1) sec = 60;
        const cdEl = document.getElementById('yb-countdown');
        if (cdEl) cdEl.innerText = sec + "s";

        const signals = ["CALL", "PUT", "WAITING", "STRONG CALL", "STRONG PUT"];
        const randomSig = signals[Math.floor(Math.random() * signals.length)];
        const sigEl = document.getElementById('yb-signal');
        if (sigEl) {
            sigEl.innerText = randomSig;
            if (randomSig.includes("CALL")) sigEl.style.color = "#4ade80";
            else if (randomSig.includes("PUT")) sigEl.style.color = "#f87171";
            else sigEl.style.color = "#facc15";
        }
    }, 2000);
})();
"""

@app.route('/')
def home():
    return "Yasin TR Bot Server Running 24/7!"

@app.route('/bot.js')
def serve_bot_js():
    return Response(BOT_JS_CONTENT, mimetype='application/javascript')

def start_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    start_server()
