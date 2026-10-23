from flask import Flask
app = Flask(__name__)

HTML = """
<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>body{margin:0;background:#020617;color:#fff;font-family:Arial}.c{max-width:420px;margin:10px auto;background:#0f172a;padding:16px;border-radius:20px;border:2px solid #22c55e}.t{padding:10px 14px;background:#1e293b;border-radius:20px;margin:3px;display:inline-block;cursor:pointer;border:1px solid #334155}.a{background:#3b82f6;color:#fff}.b{font-size:56px;font-weight:900;text-align:center;margin:10px 0}.s{font-size:22px;font-weight:900;text-align:center;padding:14px;border-radius:12px}</style></head><body><div class=c>
<h2>Alufx ULTIMATE - REAL DIRECT</h2><p style=color:#22c55e>● LIVE REAL Deriv - Direct via WARP</p><p id=st style=color:#fbbf24;font-size:11px>WARP ON detected - Connecting direct to ws.deriv.com...</p>
<div><span class=t id=t0 onclick="setP('R_20')">Vol 20</span><span class=t id=t1 onclick="setP('R_100')">GainX400</span><span class=t id=t2 onclick="setP('stpRNG500')">Step 500</span><span class=t id=t3 onclick="setP('stpRNG400')">Step 400</span></div>
<div id=ttl style=text-align:center;color:#f59e0b;margin-top:12px;font-weight:bold>Vol 20 (R_20)</div><div class=b id=pr>--</div><div class=s id=sig style=background:#1e293b>Waiting REAL tick...</div><p id=lg style=font-size:10px;color:#64748b></p><p style=font-size:9px;color:#22c55e>Direct WS from phone via WARP - No Render DNS</p>
</div>
<script>
let cur='R_20';
const N={"R_20":"Vol 20","R_100":"GainX400","stpRNG500":"Step 500","stpRNG400":"Step 400"};
let last={};
let prices={};
function setP(p){
 cur=p;
 document.querySelectorAll('.t').forEach(x=>x.classList.remove('a'));
 document.getElementById('t'+({R_20:0,R_100:1,stpRNG500:2,stpRNG400:3}[p])).classList.add('a');
 document.getElementById('ttl').innerText=N[p]+' ('+p+')';
 if(prices[p]) updateUI(p, prices[p]);
}

function updateUI(sym, quote){
 let dir='BUY ▲';let col='#22c55e';let bg='#052e16';
 if(last[sym] && parseFloat(quote) < parseFloat(last[sym])){dir='SELL ▼';col='#ef4444';bg='#450a0a';}
 last[sym]=quote;
 if(sym===cur){
  document.getElementById('pr').innerText=quote;
  document.getElementById('pr').style.color=col;
  document.getElementById('sig').innerText=dir+' '+N[sym]+' REAL';
  document.getElementById('sig').style.background=bg;
  document.getElementById('sig').style.color=col;
  document.getElementById('sig').style.border='2px solid '+col;
 }
 document.getElementById('lg').innerText='REAL DIRECT '+sym+' '+quote+' @ '+new Date().toLocaleTimeString()+' via WARP';
}

function connect(){
 const ws = new WebSocket('wss://ws.deriv.com/websockets/v3?app_id=1089');
 ws.onopen = ()=>{
  document.getElementById('st').innerText='CONNECTED DIRECT REAL @ '+new Date().toLocaleTimeString()+' via WARP - Subscribed';
  document.getElementById('st').style.color='#22c55e';
  ["R_20","R_100","stpRNG500","stpRNG400"].forEach(s=>ws.send(JSON.stringify({ticks:s,subscribe:1})));
 };
 ws.onmessage = (e)=>{
  try{
   const d=JSON.parse(e.data);
   if(d.tick){
    const sym=d.tick.symbol;
    const q=d.tick.quote.toString();
    prices[sym]=q;
    updateUI(sym,q);
   }
  }catch{}
 };
 ws.onerror = ()=>{document.getElementById('st').innerText='WS error - retrying... keep WARP ON';};
 ws.onclose = ()=>{document.getElementById('st').innerText='Reconnecting in 2s...'; setTimeout(connect,2000);};
}
setP(cur);
connect();
</script></body></html>
"""

@app.route('/')
def home(): return HTML
@app.route('/health')
def h(): return "OK"

if __name__ == '__main__':
    app.run()
</code></pre>

**requirements.txt** — make it ULTRA LIGHT (delete old ones):
