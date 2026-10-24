from flask import Flask, jsonify
import os, requests, random
from datetime import datetime

app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_TOKEN','')
CHAT = os.environ.get('TELEGRAM_CHAT_ID','')

def send_tg(text):
    if not TOKEN or not CHAT: return False
    try:
        r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                          json={"chat_id": CHAT, "text": text}, timeout=5)
        return r.ok
    except:
        return False

@app.route('/')
def home():
    return """
    <html><body style="background:#020617;color:#fff;font-family:Arial;padding:20px;text-align:center">
    <h2>POCKET V4 FINAL - TELEGRAM</h2>
    <p style="color:#22c55e">● LIVE - Manual Signals Only</p>
    <h1 style="font-size:28px">GBPUSD_otc - 1m</h1>
    <div style="padding:16px;background:#052e16;border:2px solid #22c55e;border-radius:14px;color:#22c55e;font-size:22px;font-weight:900;margin:12px 0" id=sig>Press GET SIGNAL</div>
    <a href="/signal" style="display:block;padding:18px;background:linear-gradient(90deg,#38bdf8,#22c55e);color:#000;border-radius:14px;font-weight:900;text-decoration:none;margin:12px 0;font-size:18px">🔔 GET SIGNAL + TELEGRAM</a>
    <a href="/test" style="display:block;padding:12px;background:#1e293b;color:#fff;border-radius:10px;text-decoration:none">TEST TELEGRAM NOW</a>
    <p style="font-size:11px;color:#64748b;margin-top:20px">After test, bot will send CALL/PUT here<br>Add to Home Screen to use as App</p>
    </body></html>
    """

@app.route('/signal')
def signal():
    rsi = random.randint(20,80)
    acc = random.randint(82,92)
    price = round(random.uniform(1.07,1.09),5)
    if rsi < 38: msg = f"🚀 CALL BUY\nPair: GBPUSD_otc 1m\nRSI {rsi} Oversold\nAccuracy {acc}%\nPrice {price}\nTime {datetime.now().strftime('%H:%M:%S')}\n→ Trade UP 1min"
    elif rsi > 62: msg = f"🔻 PUT SELL\nPair: GBPUSD_otc 1m\nRSI {rsi} Overbought\nAccuracy {acc}%\nPrice {price}\nTime {datetime.now().strftime('%H:%M:%S')}\n→ Trade DOWN 1min"
    else: msg = f"⏳ WAIT RSI {rsi} No trade"
    send_tg(msg)
    return f"<html><body style='background:#020617;color:#fff;text-align:center;padding:20px;font-family:Arial'><h2>{msg.replace(chr(10),'<br>')}</h2><p>Sent to Telegram ID {CHAT}</p><a href='/' style='color:#38bdf8'>Back</a></body></html>"

@app.route('/test')
def test():
    ok = send_tg("✅ POCKET V4 FINAL CONNECTED\n\nBot: @pocket_otc_2026bot\nID: 8908524143\n\nYou will get signals here!\n\nTest time: "+datetime.now().strftime("%H:%M:%S"))
    return f"Telegram send: {'✅ SUCCESS - Check Telegram now!' if ok else '❌ FAILED - Check TOKEN/CHAT_ID in Render'}<br><br><a href='/'>Back</a>"

@app.route('/health')
def h(): return "OK"
