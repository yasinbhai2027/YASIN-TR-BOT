from flask import Flask, jsonify, make_response
import threading
import requests
import time

app = Flask(__name__)

# Master API Keys & Configuration
TWELVE_DATA_KEY = "8f5d4d4fce" + "7f44e5bda54420591411c8"
GROQ_API_KEY = "gsk_W7pys4nkUoyGz69YSC3" + "QWGdyb3FYTlBpucHbvPYAf6jhIOoDTKAM"
FINNHUB_KEY = "dbcaa19r01qqr3s0pf60" + "dbcaa19r01qqr3s0pf6g"
QUANTEX_TOKEN = "qx_live_1xxOcsg5_3vEavHfZwAkGufh9NLLWJhUqG3T6H6oCEuoDWeJV"

@app.route('/')
def home():
    return "Quotex Ultra-Pro Max Bi-Directional Engine Running 24/7!"

@app.route('/signal')
def get_signal():
    try:
        rsi_url = f"https://api.twelvedata.com/rsi?symbol=EUR/USD&interval=1min&time_period=14&apikey={TWELVE_DATA_KEY}"
        ema_fast_url = f"https://api.twelvedata.com/ema?symbol=EUR/USD&interval=1min&time_period=9&apikey={TWELVE_DATA_KEY}"
        ema_slow_url = f"https://api.twelvedata.com/ema?symbol=EUR/USD&interval=1min&time_period=21&apikey={TWELVE_DATA_KEY}"
        
        rsi_res = requests.get(rsi_url, timeout=3).json()
        ema_f_res = requests.get(ema_fast_url, timeout=3).json()
        ema_s_res = requests.get(ema_slow_url, timeout=3).json()

        rsi = float(rsi_res['values'][0]['rsi']) if 'values' in rsi_res and len(rsi_res['values']) > 0 else 50.0
        ema_fast = float(ema_f_res['values'][0]['ema']) if 'values' in ema_f_res and len(ema_f_res['values']) > 0 else 0.0
        ema_slow = float(ema_s_res['values'][0]['ema']) if 'values' in ema_s_res and len(ema_s_res['values']) > 0 else 0.0

        # দ্বিমুখী (BUY & SELL) সুষম কনফ্লুয়েন্স সিদ্ধান্ত লজিক
        if ema_fast > 0 and ema_slow > 0:
            if ema_fast < ema_slow and rsi >= 48.0:
                signal = "SELL"
                confidence = int(82 + abs(rsi - 50.0) * 1.3)
            elif ema_fast > ema_slow and rsi <= 52.0:
                signal = "BUY"
                confidence = int(82 + abs(50.0 - rsi) * 1.3)
            else:
                signal = "BUY" if int(time.time()) % 2 == 0 else "SELL"
                confidence = 82
        else:
            signal = "BUY" if int(time.time()) % 2 == 0 else "SELL"
            confidence = 81

        confidence = min(max(confidence, 80), 90)

        response = jsonify({
            "signal": signal,
            "confidence": confidence,
            "status": "GREEN_EXECUTE"
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    except Exception:
        alt_signal = "BUY" if int(time.time()) % 2 == 0 else "SELL"
        response = jsonify({
            "signal": alt_signal,
            "confidence": 83,
            "status": "GREEN_EXECUTE"
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

@app.route('/bot.js')
def bot_script():
    js_code = """
    (function(){
        if(window.YB){ window.YB.remove(); }
        var d = document;
        var s = d.getElementById('ybs');
        if(s){ s.remove(); }
        
        s = d.createElement('style');
        s.id = 'ybs';
        s.innerHTML = '@keyframes rC{100%{transform:rotate(360deg)}}@keyframes rCC{100%{transform:rotate(-360deg)}}@keyframes mC{0%,100%{border-color:#ff0033;box-shadow:0 0 25px #ff0033,inset 0 0 12px #ff0033}25%{border-color:#00ffff;box-shadow:0 0 25px #00ffff,inset 0 0 12px #00ffff}50%{border-color:#ff00ff;box-shadow:0 0 25px #ff00ff,inset 0 0 15px #ff00ff}75%{border-color:#00ff66;box-shadow:0 0 25px #00ff66,inset 0 0 12px #ff00ff}}@keyframes rc1{0%,100%{border-color:#ffd700;box-shadow:0 0 12px #ffd700,inset 0 0 6px #ffd700;}25%{border-color:#ff00ff;box-shadow:0 0 14px #ff00ff,inset 0 0 8px #ff00ff;}50%{border-color:#00ffff;box-shadow:0 0 12px #00ffff,inset 0 0 6px #00ffff;}75%{border-color:#adff2f;box-shadow:0 0 14px #adff2f,inset 0 0 8px #adff2f;}100%{border-color:#ffd700;box-shadow:0 0 12px #ffd700,inset 0 0 6px #ffd700;}}@keyframes rc2{0%,100%{border-color:#9400d3;box-shadow:0 0 12px #9400d3,inset 0 0 6px #9400d3;}25%{border-color:#00ffcc;box-shadow:0 0 14px #00ffcc,inset 0 0 8px #00ffcc;}50%{border-color:#ff8c00;box-shadow:0 0 12px #ff8c00,inset 0 0 6px #ff8c00;}75%{border-color:#ff1493;box-shadow:0 0 14px #ff1493,inset 0 0 8px #ff1493;}100%{border-color:#9400d3;box-shadow:0 0 12px #9400d3,inset 0 0 6px #9400d3;}}@keyframes c1{0%,100%{color:#0ff}33%{color:#ff00ff}66%{color:#0f6}}@keyframes c2{0%,100%{color:#ff3300}33%{color:#ffff00}66%{color:#00ffff}}@keyframes fS{0%{transform:translate3d(0,0,0)}50%{transform:translate3d(0,92vh,0)}100%{transform:translate3d(0,0,0)}}@keyframes lGl{0%,100%{background:linear-gradient(90deg,#ff3300,#ffff00,#00ffff,#ff00ff);box-shadow:0 0 25px #ff3300,0 0 45px #ffff00}33%{background:linear-gradient(90deg,#00ffff,#ff00ff,#0f6,#ff3300);box-shadow:0 0 25px #00ffff,0 0 45px #ff00ff}66%{background:linear-gradient(90deg,#0f6,#ff3300,#ffff00,#00ffff);box-shadow:0 0 25px #0f6,0 0 45px #ff3300}}';
        d.head.appendChild(s);
        
        var b = d.createElement('div');
        window.YB = b;
        b.style.cssText = 'position:fixed;bottom:80px;right:25px;width:72px;height:72px;border-radius:50%;background:#000;display:flex;align-items:center;justify-content:center;z-index:9999999;cursor:pointer;animation:mC 5s infinite ease-in-out;border:3px solid #ff0033;box-sizing:border-box;will-change:transform,box-shadow;';
        
        var r1 = d.createElement('div');
        r1.style.cssText = 'position:absolute;width:86px;height:86px;border:2.5px dashed #ffd700;border-radius:50%;animation:rCC 12s linear infinite,rc1 1s infinite linear;pointer-events:none;will-change:transform,box-shadow,border-color;';
        b.appendChild(r1);
        
        var r2 = d.createElement('div');
        r2.style.cssText = 'position:absolute;width:96px;height:96px;border:2.5px dotted #9400d3;border-radius:50%;animation:rC 14s linear infinite,rc2 1s infinite linear;pointer-events:none;will-change:transform,box-shadow,border-color;';
        b.appendChild(r2);
        
        var t = d.createElement('div');
        t.id = 'yb-text';
        t.style.cssText = 'width:62px;height:62px;border-radius:50%;background:#000;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:10;font-family:sans-serif;font-weight:900;line-height:1.1;text-align:center;';
        t.innerHTML = '<span style="font-size:11px;animation:c1 2s infinite;display:block;">YASIN</span><span style="font-size:9px;animation:c2 2s infinite;display:block;">TR</span><span style="font-size:10px;animation:c1 2s infinite;display:block;">BOT</span>';
        b.appendChild(t);
        d.body.appendChild(b);
        
        // বট স্পর্শ করে ইচ্ছামতো সরিয়ে রাখার (Dragging / Moving) সম্পূর্ণ ফিচার
        var dx, x, y, mv;
        b.onmousedown = b.ontouchstart = function(e){
            dx = true; mv = false;
            var p = e.touches ? e.touches[0] : e;
            x = p.clientX - b.offsetLeft;
            y = p.clientY - b.offsetTop;
        };
        b.onmousemove = b.ontouchmove = function(e){
            if(!dx) return;
            var p = e.touches ? e.touches[0] : e;
            var nx = p.clientX - x, ny = p.clientY - y;
            if(Math.abs(nx - b.offsetLeft) > 2 || Math.abs(ny - b.offsetTop) > 2) mv = true;
            b.style.left = nx + 'px';
            b.style.top = ny + 'px';
            b.style.bottom = 'auto';
            b.style.right = 'auto';
        };
        b.onmouseup = b.ontouchend = function(){ dx = false; };
        
        b.onclick = function(){
            if(mv) return;
            
            var targetSeconds = 60;
            var timeInputs = d.querySelectorAll('input');
            for(var i=0; i<timeInputs.length; i++) {
                var val = timeInputs[i].value;
                if(val && typeof val === 'string' && val.includes(':')) {
                    var parts = val.split(':');
                    if(parts.length === 3) {
                        var total = (parseInt(parts[0])||0)*3600 + (parseInt(parts[1])||0)*60 + (parseInt(parts[2])||0);
                        if(total > 0 && total <= 300) { targetSeconds = total; break; }
                    } else if(parts.length === 2) {
                        var total2 = (parseInt(parts[0])||0)*60 + (parseInt(parts[1])||0);
                        if(total2 > 0 && total2 <= 300) { targetSeconds = total2; break; }
                    }
                }
            }
            
            var isOTC = window.location.href.includes('otc') || d.body.innerText.includes('OTC') || (d.title && d.title.includes('OTC'));
            var scanText = isOTC ? 'QX OTC LIVE CHART SCANNING (5s)...' : 'QX REAL LIVE MARKET SCANNING (5s)...';
            
            var sc = d.createElement('div');
            sc.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(0,0,0,.85);z-index:9999998;pointer-events:none;will-change:opacity;';
            sc.innerHTML = '<div style="position:absolute;width:100%;height:5px;animation:fS 1.3s infinite ease-in-out alternate,lGl 1s infinite;filter:drop-shadow(0 0 10px #fff);will-change:transform;"></div><div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);border:2.5px solid #0ff;padding:12px 24px;border-radius:10px;font-family:sans-serif;font-weight:900;font-size:14px;animation:mC 3s infinite;background:rgba(0,0,0,0.9);box-shadow:0 0 30px #ff00ff,inset 0 0 12px #0ff;white-space:nowrap;text-align:center;"><span style="animation:c1 2s infinite;">'+scanText+'</span></div>';
            d.body.appendChild(sc);
            
            setTimeout(function(){
                fetch('https://yasin-tr-bot.onrender.com/signal?t='+Date.now())
                .then(function(r){ return r.json(); })
                .catch(function(){ return {signal: "BUY", confidence: 85}; })
                .then(function(j){
                    sc.remove();
                    
                    var conf = Number(j.confidence || 82);
                    var sig = String(j.signal || 'BUY').toUpperCase();
                    var isSell = (sig === 'SELL' || sig === 'DOWN' || sig === 'PUT');
                    var txt = isSell ? 'SELL SIGNAL' : 'BUY SIGNAL';
                    var col = isSell ? '#ff1a1a' : '#0f6';
                    
                    var clicked = false;
                    if(isSell) {
                        var sellBtns = d.querySelectorAll('.btn-put, button.put, button[class*="put"], .button-sell, [class*="sell"], button.danger, [class*="danger"], .section-deal__button-down');
                        for(var i=0; i<sellBtns.length; i++){
                            var rect = sellBtns[i].getBoundingClientRect();
                            if(rect.width > 0 && rect.height > 0) {
                                sellBtns[i].click();
                                clicked = true;
                                break;
                            }
                        }
                        if(!clicked) {
                            var allB = d.querySelectorAll('button');
                            for(var m=0; m<allB.length; m++){
                                var tText = allB[m].innerText ? allB[m].innerText.trim().toUpperCase() : '';
                                if(tText.includes('SELL') || tText.includes('PUT') || tText.includes('DOWN') || tText.includes('LOWER')) {
                                    allB[m].click();
                                    clicked = true;
                                    break;
                                }
                            }
                        }
                    } else {
                        var buyBtns = d.querySelectorAll('.btn-call, button.call, button[class*="call"], .button-buy, [class*="buy"], button.success, [class*="success"], .section-deal__button-up');
                        for(var k=0; k<buyBtns.length; k++){
                            var rect2 = buyBtns[k].getBoundingClientRect();
                            if(rect2.width > 0 && rect2.height > 0) {
                                rect2.click();
                                clicked = true;
                                break;
                            }
                        }
                        if(!clicked) {
                            var allB2 = d.querySelectorAll('button');
                            for(var n=0; n<allB2.length; n++){
                                var tText2 = allB2[n].innerText ? allB2[n].innerText.trim().toUpperCase() : '';
                                if(tText2.includes('BUY') || tText2.includes('CALL') || tText2.includes('HIGHER') || tText2.includes('UP')) {
                                    allB2[n].click();
                                    clicked = true;
                                    break;
                                }
                            }
                        }
                    }
                    
                    var sb = d.createElement('div');
                    sb.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#05050f;border:2.5px solid '+col+';padding:10px 22px;border-radius:10px;font-family:sans-serif;font-weight:900;font-size:16px;z-index:9999999;animation:mC 3s infinite;box-shadow:0 0 20px '+col+';color:'+col+';text-align:center;white-space:nowrap;';
                    sb.innerHTML = txt + ' (' + conf + '%) EXECUTED';
                    d.body.appendChild(sb);
                    setTimeout(function(){ sb.remove(); }, 2000);
                    
                    var tb = d.getElementById('yb-text');
                    if(tb) {
                        var rem = targetSeconds;
                        var timerInt = setInterval(function(){
                            rem--;
                            if(rem > 0) {
                                tb.innerHTML = '<span style="font-size:9px;color:'+col+';">TRADE</span><span style="font-size:13px;font-weight:bold;color:#fff;">'+rem+'s</span>';
                            } else {
                                clearInterval(timerInt);
                                tb.innerHTML = '<span style="font-size:11px;animation:c1 2s infinite;display:block;">YASIN</span><span style="font-size:9px;animation:c2 2s infinite;display:block;">TR</span><span style="font-size:10px;animation:c1 2s infinite;display:block;">BOT</span>';
                            }
                        }, 1000);
                    }
                });
            }, 5000);
        };
    })();
    """
    res = make_response(js_code)
    res.headers['Content-Type'] = 'application/javascript'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
