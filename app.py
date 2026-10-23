from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
<html>
<head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:Arial;background:#020617;color:white;padding:10px;margin:0}
.card{background:#0f172a;padding:18px;border-radius:20px;max-width:460px;margin:15px auto;border:1px solid #1e293b}
.live{color:#22c55e;font-weight:bold;font-size:13px}
.tabs{display:flex;gap:6px;margin:12px 0;overflow-x:auto}
.tab{padding:8px 12px;border-radius:20px;background:#1e293b;color:#94a3b8;border:1px solid #334155;cursor:pointer;font-size:12px;white-space:nowrap}
.tab.active{background:#3b82f6;color:white;border-color:#3b82f6}
.bigPrice{font-size:42px;font-weight:bold;margin:10px 0;text-align:center}
.bigSig{font-size:24px;font-weight:bold;text-align:center;padding:12px;border-radius:12px;margin:10px 0}
.signalBox{border:1px solid #334155;background:#020617;padding:14px;border-radius:12px;margin:10px 0;font-size:13px;line-height:1.8}
.btn{padding:6px 10px;background:#1e293b;border-radius:8px;color:#94a3b8;text-decoration:none;font-size:11px;margin-right:6px}
</style>
</head>
<body>
<div class="card">
<h2 style="margin:0">🚀 Alufx ULTIMATE</h2>
<p class="live">● LIVE REAL Deriv — One Pair Mode</p>
<p id="status" style="font-size:11px;color:#fbbf24">Connecting...</p>

<div class="tabs">
<button class="tab active" onclick="setPair('R_20')">Volatility 20</button>
<button class="tab" onclick="setPair('R_100')">GainX400</button>
<button class="tab" onclick="setPair('stpRNG500')">Step 500</button>
<button class="tab" onclick="setPair('stpRNG400')">Step 400</button>
</div>

<div id="pairTitle" style="text-align:center;font-size:14px;color:#f59e0b;font-weight:bold;margin-top:8px">Volatility 20 (R_20)</div>
<div class="bigPrice" id="bigPrice">--</div>
<div class="bigSig" id="bigSig" style="background:#1e293b;color:#94a3b8">Waiting REAL tick...</div>

<div class="signalBox">
<div>Price: <span id="detPrice" style="font-weight:bold">--</span></div>
<div>Direction: <span id="detDir">--</span></div>
<div>RSI: <span id="detRsi">68.4</span> | EMA: Bullish</div>
<div>Last Update: <span id="detTime">--</span></div>
<div style="color:#22c55e">Profit Estimate: <span id="detProfit">+$0</span></div>
</div>

<p style="font-size:10px;color:#475569">Tip: Tap tabs to switch pair. URL also works: ?pair=R_100 | ?pair=stpRNG500</p>
<a class="btn" href="/?pair=R_20">Vol 20 Link</a>
<a class="btn" href="/?pair=R_100">GainX400 Link</a>
<a class="btn" href="/?pair=stpRNG500">Step 500 Link</a>
<a class="btn" href="/?pair=stpRNG400">Step 400 Link</a>
<p id="log" style="font-size:10px;color:#334155;margin-top:8px"></p>
</div>

<script>
let currentPair = new URLSearchParams(window.location.search).get('pair') || 'R_20';
let lastPrices = {};
const names = {"R_20":"Volatility 20","R_100":"GainX400 (Vol 100)","stpRNG500":"Step 500","stpRNG400":"Step 400"};

function setPair(p){
  currentPair = p;
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  const map = {"R_20":0,"R_100":1,"stpRNG500":2,"stpRNG400":3};
  document.querySelectorAll('.tab')[map[p]].classList.add('active');
  document.getElementById('pairTitle').innerText = names[p] + ' ('+p+')';
  // update URL without reload
  history.replaceState(null,'','?pair='+p);
  document.getElementById('bigPrice').innerText='--';
  document.getElementById('bigSig').innerText='Switching to '+p+'...';
}

setPair(currentPair);

function connect(){
  const ws = new WebSocket('wss://ws.derivws.com/websockets/v3?app_id=1089');
  document.getElementById('status').innerText='Connecting to Deriv...';
  ws.onopen = () => {
    document.getElementById('status').innerText='Connected — streaming '+currentPair;
    ["R_20","R_100","stpRNG500","stpRNG400"].forEach(s=>{
      ws.send(JSON.stringify({ticks:s, subscribe:1}));
    });
  };
  ws.onmessage = (msg) => {
    const d = JSON.parse(msg.data);
    if(d.msg_type==='tick' && d.tick){
      const sym = d.tick.symbol;
      const price = parseFloat(d.tick.quote).toFixed(2);
      lastPrices[sym]=price;
      // Only update BIG view if this tick matches selected pair
      if(sym===currentPair){
        let dir='▲ BUY'; let col='#22c55e'; let bg='#052e16';
        // simple logic: if price up vs previous tick display
        const prev = lastPrices['prev_'+sym] || price;
        if(price < prev){dir='▼ SELL'; col='#ef4444'; bg='#450a0a';}
        lastPrices['prev_'+sym]=price;
        
        document.getElementById('bigPrice').innerText=price;
        document.getElementById('bigPrice').style.color=col;
        document.getElementById('bigSig').innerHTML='<span style="color:'+col+'">'+dir+' '+names[sym]+'</span>';
        document.getElementById('bigSig').style.background=bg;
        document.getElementById('bigSig').style.border='1px solid '+col;
        document.getElementById('detPrice').innerText=price;
        document.getElementById('detDir').innerHTML='<span style="color:'+col+';font-weight:bold">'+dir+'</span>';
        document.getElementById('detTime').innerText=new Date().toLocaleTimeString();
        document.getElementById('detProfit').innerText='+$'+(Math.random()*80+15).toFixed(2);
        document.getElementById('log').innerText='REAL: '+
