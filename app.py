import os
from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    <html>
    <head>
        <title>Alufx Bot</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial; background: #0f172a; color: white; text-align: center; padding: 50px; }}
            .card {{ background: #1e293b; padding: 30px; border-radius: 20px; max-width: 400px; margin: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
            .live {{ color: #22c55e; font-size: 22px; font-weight: bold; }}
            .btn {{ background: #3b82f6; color: white; padding: 12px 25px; border-radius: 10px; text-decoration: none; display: inline-block; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 Alufx Trading Bot</h1>
            <p class="live">● LIVE & RUNNING</p>
            <p>Your bot is deployed successfully!</p>
            <p>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <a class="btn" href="/status">Check Status</a>
        </div>
    </body>
    </html>
    """

@app.route('/status')
def status():
    return {"status": "live", "bot": "Alufx", "uptime": "100%", "message": "Bot is working perfectly!"}

@app.route('/health')
def health():
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
