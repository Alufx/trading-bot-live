from flask import Flask
app = Flask(__name__)
HTML = """<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{font-family:Arial;background:#020617;color:#fff;padding:10px}.card{background:#0f172a;padding:18px;border-radius:20px;max-width:460px;margin:auto;border:1px solid #1e293b}.tab{padding:8px 12px;border-radius:20px;background:#1e293b;color:#94a3b8;border:1px solid #334155;cursor:pointer;font-size:12px;margin:3px;display:inline-block}.tab.active{background:#3b82f6;color:#fff}.big{font-size:48px;font-weight:bold;text-align:center;margin:14px 0}.sig{font-size:22px;font-weight:bold;text-align:center;padding:14px;border-radius:12px}</style></head><body><div class=card><h2>Alufx ULTIMATE</h2><p style=color:#22c55e>LIVE REAL Deriv - ONE PAIR</p><p id=status style=color:#fbbf24;font-size:11px>Init...</p><div><span class=tab id=t0 onclick=setPair('R_20')>Vol 20</span><span class=tab id=t1 onclick=setPair('R_100')>GainX400</span><span class=tab id=t2 onclick=setPair('stpRNG500')>Step 500</span><span class=tab id=t3 onclick=setPair('stpRNG400')>Step 400</span></div><div id=title style=text-align:center;color:#f59e0b;margin-top:12px;font-weight:bold>Volatility 20</div><div class=big id=bigPrice>--</div><div class=sig id=bigSig style=background:#1e293b>Waiting REAL tick...</div><p id=log style=font-size:10px;color:#64748b;margin-top:10px;word-break:break-all></p><p style=font-size:10px;color:#475569>Direct: ?pair=R_20 | R_100 | stpRNG500 | stpRNG400</p></div><script>
let cur=new URLSearchParams(location.search).get('pair')||'R_20'; const names={"R_20":"Volatility 20 (R_20)","R_100":"GainX400 (R_100)","stpRNG500":"Step 500","stpRNG400":"Step 400"};
function setPair(p){cur=p; document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active')); const m={"R_20":0,"R_100":1,"stpRNG500":2,"stpRNG400":3}; document.getElementById('t'+m[p]).classList.add('active'); document.getElementById('title').innerText=names[p]; history.replaceState(null,'','?pair='+p); document.getElementById('bigPrice').innerText='--'; document.getElementById('log').innerText='Switched to '+p+' - subscribing...'; subscribe();}
setPair(cur);
let ws=null; let tried=0;
function subscribe(){if(ws && ws.readyState===1){["R_20","R_100","stpRNG500","stpRNG400"].forEach(s=>ws.send(JSON.stringify({ticks:s,subscribe:1})));}}
function conn(){
 const endpoints=['wss://ws.derivws.com/websockets/v3?app_id=1089','wss://ws.binaryws.com/websockets/v3?app_id=1089'];
 const url=endpoints[tried%2];
 document.getElementById('status').innerText='Connecting to '+url.substring(8,22)+'... try '+(tried+1);
 document.getElementById('log').innerText='Connecting '+url;
 try{ws=new WebSocket(url);}catch(e){document.getElementById('log').innerText='WS error: '+e; tried++; setTimeout(conn,1500); return;}
 ws.onopen=()=>{document.getElementById('status').innerText='Connected to Deriv! Subscribing...'; document.getElementById('log').innerText='Connected '+url+' - sending ticks'; subscribe();};
 ws.onmessage=(e)=>{try{const d=JSON.parse(e.data); document.getElementById('log').innerText='Msg: '+e.data.substring(0,120); if(d.tick){const s=d.tick.symbol; const pr=parseFloat(d.tick.quote).toFixed(2); if(s===cur){let dir='BUY ▲'; let col='#22c55e'; let bg='#052e16'; const prev=window['_'+s]||pr; if(pr<prev){dir='SELL ▼'; col='#ef4444'; bg='#450a0a';} window['_'+s]=pr; document.getElementById('bigPrice').innerText=pr; document.getElementById('bigPrice').style.color=col; document.getElementById('bigSig').innerText=dir+' '+names[s]; document.getElementById('bigSig').style.background=bg; document.getElementById('bigSig').style.color=col; document.getElementById('bigSig').style.border='2px solid '+col; document.getElementById('status').innerText='LIVE REAL '+s+' '+pr;}}}catch(err){document.getElementById('log').innerText='Parse err: '+err;}};
 ws.onerror=()=>{document.getElementById('status').innerText='WS Error - retrying'; document.getElementById('log').innerText='WS Error '+url; tried++; setTimeout(conn,1500);};
 ws.onclose=()=>{document.getElementById('status').innerText='Closed - reconnect'; tried++; setTimeout(conn,1500);};
}
conn();
</script></body></html>"""
@app.route('/')
def home():
    return HTML
@app.route('/health')
def health():
    return "OK"
