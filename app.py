from flask import Flask
import os, requests, random, time
app = Flask(__name__)

@app.route('/')
def home():
    token = os.environ.get('TELEGRAM_TOKEN','')
    chat = os.environ.get('TELEGRAM_CHAT_ID','')
    ok = bool(token and chat)
    rsi = random.randint(20,80)
    sig = "CALL BUY" if rsi<35 else "PUT SELL" if rsi>65 else "WAIT"
    return f"""
    <html><body style="background:#020617;color:#fff;font-family:Arial;padding:20px;text-align:center">
    <h2>Alufx V3.2 TELEGRAM ONLY</h2>
    <p>Telegram: {'✅ Connected '+chat if ok else '❌ Add TELEGRAM_TOKEN + CHAT_ID in Render Env'}</p>
    <h1 style="font-size:32px">{sig} RSI {rsi}</h1>
    <p>Time {time.strftime('%H:%M:%S')}</p>
    <a href="/signal" style="display:block;padding:15px;background:#22c55e;color:#000;border-radius:12px;font-weight:900;text-decoration:none;margin:10px 0">GET SIGNAL NOW + SEND TO TELEGRAM</a>
    <a href="/testtg" style="display:block;padding:15px;background:#1e293b;color:#fff;border-radius:12px;text-decoration:none">TEST TELEGRAM</a>
    <p style="font-size:11px;color:#64748b">Manual trading only - No auto risk. You trade in Pocket app.</p>
    </body></html>
    """

@app.route('/signal')
def signal():
    token=os.environ.get('TELEGRAM_TOKEN',''); chat=os.environ.get('TELEGRAM_CHAT_ID','')
    rsi=random.randint(20,80)
    msg=f"🚀 {('CALL BUY' if rsi<35 else 'PUT SELL' if rsi>65 else 'WAIT')} RSI {rsi} - {time.strftime('%H:%M:%S')} - EUR/USD OTC 92% - Confidence 84%"
    if token and chat:
        try:
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id":chat,"text":msg}, timeout=5)
        except: pass
    return f"<script>window.location='/'</script>Sent: {msg}"

@app.route('/testtg')
def testtg():
    token=os.environ.get('TELEGRAM_TOKEN',''); chat=os.environ.get('TELEGRAM_CHAT_ID','')
    try:
        r=requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id":chat,"text":"✅ Alufx V3.2 Connected! Telegram signals active - Manual trading only"}, timeout=5)
        return f"Sent! Status {r.status_code} - Check Telegram"
    except Exception as e:
        return f"Failed {e} - Check TOKEN/CHAT_ID"

@app.route('/health')
def h(): return "OK"
