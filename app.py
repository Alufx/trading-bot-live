from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>body{margin:0;background:#020617;color:#fff;font-family:Arial}.c{max-width:420px;margin:10px auto;background:#0f172a;padding:16px;border-radius:20px;border:1px solid #1e293b}.t{padding:10px 14px;background:#1e293b;border-radius:20px;margin:3px;display:inline-block;cursor:pointer;color:#94a3b8}.a{background:#3b82f6;color:#fff}.b{font-size:56px;font-weight:900;text-align:center;margin:8px 0}.s{font-size:24px;font-weight:900;text-align:center;padding:12px;border-radius:12px}</style></head><body><div class=c>
<h2>Alufx ULTIMATE</h2><p style=color:#22c55e>LIVE REAL - 2026 ENDPOINTS</p><p id=st style=color:#fbbf24;font-size:11px>Init...</p><p id=err style=color:#ef4444;font-size:9px;word-break:break-all></p>
<div><span class=t id=t0 onclick="setP('R_20')">Vol 20</span><span class=t id=t1 onclick="setP('R_100')">GainX400</span><span class=t id=t2 onclick="setP('stpRNG500')">Step 500</span><span class=t id=t3 onclick="setP('stpRNG400')">Step 400</span></div>
<div id=ttl style=text-align:center;color:#f59e0b;margin-top:10px>Vol 20 (R_20)</div><div class=b id=pr>--</div><div class=s id=sig style=background:#1e293b>Connecting...</div><p id=lg style=font-size:10px;color:#64748b;word-break:break-all></p>
</div><script>
let cur=new URLSearchParams(location.search).get('pair')||'R_20';
const N={"R_20":"Volatility 20","R_100":"GainX400","stpRNG500":"Step 500","stpRNG400":"Step 400"};
let last={};let ws=null;let idx=0;
const ENDPOINTS=[
 "wss://ws.deriv.com/websockets/v3?app_id=1089",
 "wss://www.deriv.com/websockets/v3?app_id=1089",
 "wss://gateway.deriv.com/websockets/v3?app_id=1089",
 "wss://ws.derivws.com/websockets/v3?app_id=1089",
 "wss://ws.binaryws.com/websockets/v3?app_id=1089",
 "wss://api.deriv.com/websockets/v3?app_id=1089"
];
function setP(p){cur=p;document.querySelectorAll('.t').forEach(x=>x.classList.remove('a'));document.getElementById('t'+({R_20:0,R_100:1,stpRNG500:2,stpRNG400:3}[p])).classList.add('a');document.getElementById('ttl').innerText=N[p]+' ('+p+')';history.replaceState(null,'','?pair='+p);if(ws)ws.close();idx=0;connect();}
function connect(){
 let url=ENDPOINTS[idx%ENDPOINTS.length];
 document.getElementById('st').innerText='Trying '+(idx+1)+'/6: '+url.slice(8,28);
 document.getElementById('err').innerText='';
 try{
  ws=new WebSocket(url);
  ws.onopen=()=>{document.getElementById('st').innerText='CONNECTED via '+url.slice(8,28)+' @ '+new Date().toLocaleTimeString(); document.getElementById('err').innerText='LIVE'; ws.send(JSON.stringify({ticks:cur,subscribe:1}));};
  ws.onmessage=e=>{try{let d=JSON.parse(e.data);if(d.error){document.getElementById('err').innerText='API error: '+d.error.message; idx++; setTimeout(connect,800); return;} if(d.tick&&d.tick.symbol===cur){let pr=d.tick.quote;let dir='BUY ▲';let col='#22c55e';let bg='#052e16';if(last[cur]&&parseFloat(pr)<parseFloat(last[cur])){dir='SELL ▼';col='#ef4444';bg='#450a0a';}last[cur]=pr;document.getElementById('pr').innerText=pr;document.getElementById('pr').style.color=col;document.getElementById('sig').innerText=dir+' '+N[cur];document.getElementById('sig').style.background=bg;document.getElementById('sig').style.color=col;document.getElementById('sig').style.border='2px solid '+col;document.getElementById('lg').innerText='REAL '+cur+' '+pr+' id:'+d.tick.id;}}catch(err){}};
  ws.onerror=ev=>{document.getElementById('err').innerText='WS error on '+url.slice(8,28)+' -> next in 1s'; idx++; setTimeout(connect,1000);};
  ws.onclose=()=>{if(document.getElementById('pr').innerText==='--'){idx++; setTimeout(connect,800);} else {document.getElementById('st').innerText='Closed, reconnecting...'; idx++; setTimeout(connect,1200);}};
 }catch(ex){document.getElementById('err').innerText='Exception '+ex; idx++; setTimeout(connect,800);}
}
setP(cur);
</script></body></html>"""
@app.route('/health')
def h(): return "OK"
