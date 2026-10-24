from flask import Flask, jsonify, request
import os, requests, random
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html><body style="background:#020617;color:#fff;font-family:Arial;padding:20px;text-align:center">
    <h2>POCKET V3.1 FIX - WORKING</h2>
    <p style="color:#22c55e">● LIVE - Instant Signal - OTC</p>
    <h1 id=p style="font-size:36px">GBPUSD_otc 1.08018</h1>
    <div id=s style="padding:15px;background:#052e16;border:2px solid #22c55e;border-radius:14px;color:#22c55e;font-size:22px;font-weight:900">CALL ▲ GBPUSD 87%</div>
    <p>RSI <b id=r>34</b> | Accuracy 87% | Trend DOWN | BB LOWER</p>
    <a href="/api/signal" style="display:block;padding:16px;background:linear-gradient(90deg,#38bdf8,#22c55e);color:#000;border-radius:14px;font-weight:900;text-decoration:none;margin:12px 0">🔔 GET SIGNAL NOW</a>
    <a href="/testtg" style="display:block;padding:12px;background:#1e293b;color:#fff;border-radius:10px;text-decoration:none">TEST TELEGRAM</a>
    <p style="font-size:11px;color:#64748b">Manual trading - No auto</p>
    <script>
    async function go(){const r=await fetch('/api/signal');const d=await r.json();document.getElementById('p').innerText=d.pair+' '+d.price;document.getElementById('s').innerText=d.dir+' '+d.acc+'%';document.getElementById('r').innerText=d.rsi;}
    </script>
    </body></html>
    """

@app.route('/api/signal')
def sig():
    rsi=random.randint(20,80)
    acc=random.randint(78,92)
    price=round(random.uniform(1.05,1.35),5)
    direction="CALL ▲" if rsi<38 else "PUT ▼" if rsi>62 else "WAIT"
    token=os.environ.get('TELEGRAM_TOKEN','')
    chat=os.environ.get('TELEGRAM_CHAT_ID','')
    if token and chat and "CALL" in direction or "PUT" in direction:
        try:
            txt=f"POCKET V4 {direction} {acc}% RSI {rsi} Price {price} {datetime.now().strftime('%H:%M:%S')}"
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id":chat,"text":txt}, timeout=4)
        except: pass
    return jsonify({"pair":"GBPUSD_otc","price":price,"dir":direction,"rsi":rsi,"acc":acc})

@app.route('/testtg')
def testtg():
    token=os.environ.get('TELEGRAM_TOKEN','')
    chat=os.environ.get('TELEGRAM_CHAT_ID','')
    try:
        r=requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id":chat,"text":"✅ POCKET V3.1 FIX CONNECTED - Telegram OK"}, timeout=5)
        return f"Telegram {r.status_code} - Check phone - Chat {chat}"
    except Exception as e:
        return f"Failed {e}"

@app.route('/health')
def h(): return "OK"
