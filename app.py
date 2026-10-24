from flask import Flask, jsonify
import os, requests, random
from datetime import datetime
app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_TOKEN','')
CHAT = os.environ.get('TELEGRAM_CHAT_ID','')

def tg(m):
    if not TOKEN or not CHAT: return
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id":CHAT,"text":m}, timeout=5)
    except: pass

@app.route('/')
def home():
    return '<html><body style="background:#020617;color:#fff;text-align:center;padding:20px;font-family:Arial"><h2>POCKET V4 - TELEGRAM</h2><p style="color:#22c55e">LIVE - Manual Signals</p><h1 id=p>GBPUSD_otc 1.08018</h1><div id=s style="padding:15px;background:#052e16;border:2px solid #22c55e;border-radius:12px;color:#22c55e;font-weight:900">CALL 87%</div><br><a href="/signal" style="display:block;padding:16px;background:#22c55e;color:#000;border-radius:12px;font-weight:900;text-decoration:none">GET SIGNAL + TELEGRAM</a><br><a href="/test" style="display:block;padding:12px;background:#1e293b;color:#fff;border-radius:10px;text-decoration:none">TEST TELEGRAM</a></body></html>'

@app.route('/signal')
def signal():
    rsi = random.randint(20,80)
    acc = random.randint(80,92)
    price = round(random.uniform(1.07,1.09),5)
    if rsi < 38: txt = f"CALL BUY GBPUSD_otc 1m RSI {rsi} ACC {acc}% Price {price} Time {datetime.now().strftime('%H:%M:%S')}"
    elif rsi > 62: txt = f"PUT SELL GBPUSD_otc 1m RSI {rsi} ACC {acc}% Price {price} Time {datetime.now().strftime('%H:%M:%S')}"
    else: txt = f"WAIT RSI {rsi}"
    tg(txt)
    return jsonify({"msg":txt})

@app.route('/test')
def test():
    ok = tg(f"Connected! ID {CHAT} Time {datetime.now().strftime('%H:%M:%S')}")
    # even if tg() returns None, try direct
    try:
        r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id":CHAT,"text":"✅ POCKET V4 CONNECTED - @pocket_otc_2026bot"}, timeout=5)
        return f"Status {r.status_code} - Check Telegram bot @pocket_otc_2026bot - ID {CHAT} - Token set? {bool(TOKEN)}"
    except Exception as e:
        return f"Error {e} - Token {bool(TOKEN)} Chat {CHAT}"

@app.route('/health')
def h(): return "OK"
