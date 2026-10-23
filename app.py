from flask import Flask
app = Flask(__name__)

HTML='''<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;background:#020617;color:#fff;font-family:Arial}.c{max-width:430px;margin:12px auto;background:#0f172a;padding:16px;border-radius:20px;border:2px solid #22c55e}.t{padding:10px 14px;background:#1e293b;border-radius:20px;margin:3px;display:inline-block;cursor:pointer}.a{background:#3b82f6;color:#fff}.b{font-size:56px;font-weight:900;text-align:center;margin:10px 0}.s{font-size:22px;font-weight:900;text-align:center;padding:14px;border-radius:12px}</style></head><body><div class=c>
<h2>Alufx ULTIMATE REAL V5</h2><p style=color:#22c55e>● LIVE REAL - Browser Direct</p><p id=st style=color:#fbbf24;font-size:11px>Connecting directly to Deriv...</p>
<div><span class=t id=t0 onclick="setP('R_20')">Vol 20</span><span class=t id=t1 onclick="setP('R_100')">GainX400</span><span class=t id=t2 onclick="setP('stpRNG500')">Step 500</span><span class=t id=t3 onclick="setP('stpRNG400')">Step 400</span></div>
<div id=ttl style=text-align:center;color:#f59e0b;margin-top:12px;font-weight:bold>Vol 20 (R_20)</div><div class=b id=pr>--</div><div class=s id=sig style=background:#1e293b>Connecting REAL...</div><p id=lg style=font-size:10px;color:#64748b></p>
</div>
<script>
let cur='R_20';const N={"R_20":"Vol 20","R_100":"GainX400","stpRNG500":"Step 500","stpRNG400":"Step 400"};let last={};let prices={};
function setP(p){cur=p;document.querySelectorAll('.t').forEach(x=>x.classList.remove('a'));document.getElementById('t'+({R_20:0,R_100:1,stpRNG500:2,stpRNG400:3}[p])).classList.add('a');document.getElementById('ttl').innerText=N[p]+' ('+p+')';upd();}
function upd(){const pr=prices[cur];if(!pr)return;let dir='BUY ▲';let col='#22c55e';let bg='#052e16';if(last[cur]&&parseFloat(pr)<parseFloat(last[cur])){dir='SELL ▼';col='#ef4444';bg='#450a0a';}last[cur]=pr;document.getElementById('pr').innerText=pr;document.getElementById('pr').style.color=col;document.getElementById('sig').innerText=dir+' '+N[cur]+' REAL';document.getElementById('sig').style.background=bg;document.getElementById('sig').style.color=col;document.getElementById('sig').style.border='2px solid '+col;}
let ws;function connect(){try{ws=new WebSocket('wss://ws.deriv.com/websockets/v3?app_id=1089');document.getElementById('st').innerText='Connecting ws.deriv.com...';ws.onopen=()=>{document.getElementById('st').innerText='CONNECTED REAL - subscribing';['R_20','R_100','stpRNG500','stpRNG400'].forEach(s=>ws.send(JSON.stringify({ticks:s,subscribe:1})));};ws.onmessage=(e)=>{try{const d=JSON.parse(e.data);if(d.tick){prices[d.tick.symbol]=d.tick.quote.toString();document.getElementById('st').innerText='LIVE REAL @ '+new Date().toLocaleTimeString()+' '+d.tick.symbol+' '+d.tick.quote+' via ws.deriv.com';document.getElementById('lg').innerText='REAL '+d.tick.symbol+' '+d.tick.quote;upd();}}catch{}};ws.onerror=(e)=>{document.getElementById('st').innerText='WS Error, retrying...';};ws.onclose=()=>{document.getElementById('st').innerText='Closed, reconnecting in 2s...';setTimeout(connect,2000);};}catch(e){document.getElementById('st').innerText='Err '+e;setTimeout(connect,2000);}}setP(cur);connect();setInterval(upd,300);
</script></body></html>'''

@app.route('/')
def home(): return HTML
@app.route('/health')
def h(): return "OK"
