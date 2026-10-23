from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>body{background:#020617;color:#fff;font-family:Arial;padding:10px}
.card{background:#0f172a;padding:18px;border-radius:22px;max-width:460px;margin:15px auto;border:1px solid #1e293b}
.tab{padding:10px 15px;background:#1e293b;border-radius:20px;margin:4px;display:inline-block;cursor:pointer;color:#94a3b8;border:1px solid #334155}
.tab.active{background:#3b82f6;color:#fff}
.big{font-size:58px;font-weight:900;text-align:center;margin:10px 0}
.sig{font-size:26px;font-weight:900;text-align:center;padding:14px;border-radius:14px}
</style></head><body>
<div class=card>
<h2>Alufx ULTIMATE</h2>
<p style=color:#22c55e>LIVE REAL Deriv - CLIENT MODE - ONE PAIR</p>
<p id=status style=color:#fbbf24;font-size:11px>Connecting...</p>
<div>
<span class=tab id=t0 onclick="setPair('R_20')">Vol 20</span>
<span class=tab id=t1 onclick="setPair('R_100')">GainX400</span>
<span class=tab id=t2 onclick="setPair('stpRNG500')">Step 500</span>
<span class=tab id=t3 onclick="setPair('stpRNG400')">Step 400</span>
</div>
<div id=title style=text-align:center;color:#f59e0b;margin-top:12px;font-weight:bold>Volatility 20</div>
<div class=big id=price>--</div>
<div class=sig id=sig style=background:#1e293b>Connecting to Deriv...</div>
<p id=log style=font-size:10px;color:#64748b></p>
<p style=font-size:9px;color:#475569>Links: ?pair=R_20 | R_100 | stpRNG500 | stpRNG400 - Client direct WS - Cannot be blocked</p>
</div>
<script>
let cur=new URLSearchParams(location.search).get('pair')||'R_20';
const names={"R_20":"Volatility 20","R_100":"GainX400","stpRNG500":"Step 500","stpRNG400":"Step 400"};
let last={}; let ws=null;
function setPair(p){
 cur=p;
 document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
 const m={"R_20":0,"R_100":1,"stpRNG500":2,"stpRNG400":3};
 document.getElementById('t'+m[p]).classList.add('active');
 document.getElementById('title').innerText=names[p]+' ('+p+')';
 history.replaceState(null,'','?pair='+p);
 if(ws){ws.close();}
 connect();
}
function connect(){
 const urls=["wss://ws.derivws.com/websockets/v3?app_id=1089","wss://ws.binaryws.com/websockets/v3?app_id=1089"];
 document.getElementById('status').innerText='Connecting to '+urls[0].slice(8,22)+'...';
 ws=new WebSocket(urls[0]);
 ws.onopen=()=>{document.getElementById('status').innerText='LIVE REAL @ '+new Date().toLocaleTimeString(); ws.send(JSON.stringify({ticks:cur,subscribe:1}));};
 ws.onmessage=(e)=>{
  try{
   const d=JSON.parse(e.data);
   if(d.tick){
     const pr=d.tick.quote; const sym=d.tick.symbol;
     if(sym!==cur) return;
     let dir='BUY ▲'; let col='#22c55e'; let bg='#052e16';
     if(last[cur] && parseFloat(pr)<parseFloat(last[cur])){dir='SELL ▼'; col='#ef4444'; bg='#450a0a';}
     last[cur]=pr;
     document.getElementById('price').innerText=pr;
     document.getElementById('price').style.color=col;
     document.getElementById('sig').innerText=dir+' '+names[cur];
     document.getElementById('sig').style.background=bg;
     document.getElementById('sig').style.color=col;
     document.getElementById('sig').style.border='2px solid '+col;
     document.getElementById('log').innerText='REAL: '+cur+' '+pr+' id:'+d.tick.id+' @ '+new Date().toLocaleTimeString();
   }
  }catch(err){}
 };
 ws.onerror=()=>{document.getElementById('status').innerText='WS error - retrying...';};
 ws.onclose=()=>{document.getElementById('status').innerText='Reconnecting...'; setTimeout(connect,1500);};
}
setPair(cur);
</script></body></html>
"""

@app.route('/health')
def h(): return "OK"
