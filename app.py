from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
<html>
<head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:Arial;background:#020617;color:white;padding:12px}
.card{background:#0f172a;padding:20px;border-radius:20px;max-width:480px;margin:auto;border:1px solid #1e293b}
.live{color:#22c55e;font-weight:bold}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.box{background:#1e293b;padding:14px;border-radius:12px;text-align:center}
.price{font-size:18px;font-weight:bold}
</style>
</head>
<body>
<div class="card">
<h2>🚀 Alufx REAL Deriv</h2>
<p class="live">● LIVE — REAL Deriv Feed — No API Key</p>
<p id="status" style="font-size:11px;color:#94a3b8">Connecting to wss://ws.derivws.com...</p>

<div class="grid">
<div class="box">Volatility 20<br><div class="price" id="p_R_20">--</div><div id="s_R_20">Wait...</div></div>
<div class="box">GainX400<br><div class="price" id="p_R_100">--</div><div id="s_R_100">Wait...</div></div>
<div class="box">Step 500<br><div class="price" id="p_stpRNG500">--</div><div id="s_stpRNG500">Wait...</div></div>
<div class="box">Step 400<br><div class="price" id="p_stpRNG400">--</div><div id="s_stpRNG400">Wait...</div></div>
</div>
<p style="font-size:11px;margin-top:12px;color:#64748b" id="log"></p>
</div>

<script>
const pairs = ["R_20","R_100","stpRNG500","stpRNG400"];
let last = {};
const ws = new WebSocket('wss://ws.derivws.com/websockets/v3?app_id=1089');

ws.onopen = () => {
  document.getElementById('status').innerText = 'Connected! Subscribing to REAL ticks...';
  pairs.forEach(s => ws.send(JSON.stringify({ticks:s})));
};

ws.onmessage = (msg) => {
  const d = JSON.parse(msg.data);
  if(d.tick){
    const sym = d.tick.symbol;
    const price = parseFloat(d.tick.quote).toFixed(2);
    const el = document.getElementById('p_'+sym);
    const sigEl = document.getElementById('s_'+sym);
    if(el){
      let dir = '▲ BUY'; let col = '#22c55e';
      if(last[sym] && price < last[sym]){dir='▼ SELL'; col='#ef4444';}
      last[sym]=price;
      el.innerText = price;
      el.style.color = col;
      sigEl.innerHTML = '<span style="color:'+col+'">'+dir+'</span>';
      document.getElementById('log').innerText = 'REAL tick: '+sym+' '+price+' @ '+new Date().toLocaleTimeString();
    }
  }
};

ws.onerror = () => { document.getElementById('status').innerText='WS Error - Refresh page'; };
ws.onclose = () => { document.getElementById('status').innerText='WS Closed - Refresh to reconnect'; };
</script>
</body>
</html>
"""

@app.route('/health')
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
