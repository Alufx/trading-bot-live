import os, json, time, threading, traceback
import websocket
from flask import Flask, jsonify

app = Flask(__name__)
PRICES = {"R_20": "--", "R_100": "--", "stpRNG500": "--", "stpRNG400": "--", "status": "starting server...", "error": "", "last_id": 0}

ENDPOINTS = [
    "wss://ws.binaryws.com/websockets/v3?app_id=1089",
    "wss://ws.derivws.com/websockets/v3?app_id=1089",
    "wss://ws.deriv.com/websockets/v3?app_id=1089"
]

def on_message(ws, msg):
    try:
        d=json.loads(msg)
        if "tick" in d:
            PRICES[d["tick"]["symbol"]]=str(d["tick"]["quote"])
            PRICES["last_id"]=d["tick"].get("id",0)
            PRICES["status"]=f"LIVE REAL SERVER @ {time.strftime('%H:%M:%S')}"
            PRICES["error"]=""
    except: pass

def on_open(ws):
    PRICES["status"]="Server connected - subscribing"
    for s in ["R_20","R_100","stpRNG500","stpRNG400"]:
        ws.send(json.dumps({"ticks": s, "subscribe": 1}))

def on_error(ws, err):
    PRICES["error"]=f"{err}"[:120]
    PRICES["status"]=f"Server WS error"

def on_close(ws,a,b):
    PRICES["status"]="Server closed - retry"

def run_ws():
    idx=0
    while True:
        url=ENDPOINTS[idx%3]
        try:
            PRICES["status"]=f"Trying {url[8:22]} #{idx+1}"
            w=websocket.WebSocketApp(url, on_message=on_message, on_open=on_open, on_error=on_error, on_close=on_close)
            w.run_forever(sslopt={"cert_reqs": 0}, ping_interval=20, ping_timeout=10)
        except Exception as e:
            PRICES["status"]=f"Server exception {e}"[:80]
        idx+=1
        time.sleep(2)

threading.Thread(target=run_ws, daemon=True).start()

HTML = """
<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>body{background:#020617;color:#fff;font-family:Arial;padding:10px}.card{background:#0f172a;padding:18px;border-radius:22px;max-width:460px;margin:15px auto;border:1px solid #1e293b}.tab{padding:10px 15px;background:#1e293b;border-radius:20px;margin:4px;display:inline-block;cursor:pointer;color:#94a3b8;border:1px solid #334155}.tab.active{background:#3b82f6;color:#fff}.big{font-size:58px;font-weight:900;text-align:center;margin:10px 0}.sig{font-size:26px;font-weight:900;text-align:center;padding:14px;border-radius:14px}</style></head><body>
<div class=card><h2>Alufx ULTIMATE</h2><p style=color:#22c55e>LIVE REAL - HYBRID FAILOVER</p><p id=status style=color:#fbbf24;font-size:11px>Loading...</p><p id=err style=color:#ef4444;font-size:9px;word-break:break-all></p><div><span class=tab id=t0 onclick="setPair('R_20')">Vol 20</span><span class=tab id=t1 onclick="setPair('R_100')">GainX400</span><span class=tab id=t2 onclick="setPair('stpRNG500')">Step 500</span><span class=tab id=t3 onclick="setPair('stpRNG400')">Step 400</span></div><div id=title style=text-align:center;color:#f59e0b;margin-top:12px;font-weight:bold>Volatility 20</div><div class=big id=price>--</div><div class=sig id=sig style=background:#1e293b>Initializing...</div><p id=log style=font-size:10px;color:#64748b;word-break:break-all></p><p style=font-size:9px;color:#475569>Auto: Server first, then Client direct if blocked - ONE PAIR ?pair=R_20 etc</p></div>
<script>
let cur=new URLSearchParams(location.search).get('pair')||'R_20';
const names={"R_20":"Volatility 20","R_100":"GainX400","stpRNG500":"Step 500","stpRNG400":"Step 400"};
let last={}; let serverOK=false; let clientWS=null; let clientActive=false;
const ENDPOINTS=["wss://ws.binaryws.com/websockets/v3?app_id=1089","wss://ws.derivws.com/websockets/v3?app_id=1089","wss://ws.deriv.com/websockets/v3?app_id=1089"];
let idx=0;

function setPair(p){
 cur=p;
 document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
 const m={"R_20":0,"R_100":1,"stpRNG500":2,"stpRNG400":3};
 document.getElementById('t'+m[p]).classList.add('active');
 document.getElementById('title').innerText=names[p]+' ('+p+')';
 history.replaceState(null,'','?pair='+p);
 last={}; document.getElementById('price').innerText='--';
 if(clientWS){clientWS.close(); clientActive=false;}
 serverOK=false;
 setTimeout(checkFailover,4000);
}

async function pollServer(){
 try{
  const r=await fetch('/api/prices?'+Date.now());
  const d=await r.json();
  if(!clientActive){
   document.getElementById('status').innerText=d.status+' [SERVER]';
   document.getElementById('err').innerText=d.error||'';
  }
  const pr=d[cur];
  if(pr && pr!=='--'){
   serverOK=true;
   if(!clientActive){ showPrice(pr, d.last_id, 'SERVER'); }
  }
 }catch(e){
  if(!clientActive) document.getElementById('status').innerText='Server fetch err '+e;
 }
}

function showPrice(pr, id, src){
 let dir='BUY ▲'; let col='#22c55e'; let bg='#052e16';
 if(last[cur] && parseFloat(pr)<parseFloat(last[cur])){dir='SELL ▼'; col='#ef4444'; bg='#450a0a';}
 last[cur]=pr;
 document.getElementById('price').innerText=pr;
 document.getElementById('price').style.color=col;
 document.getElementById('sig').innerText=dir+' '+names[cur];
 document.getElementById('sig').style.background=bg;
 document.getElementById('sig').style.color=col;
 document.getElementById('sig').style.border='2px solid '+col;
 document.getElementById('log').innerText=src+' REAL: '+cur+' '+pr+' id:'+id+' @ '+new Date().toLocaleTimeString();
}

function checkFailover(){
 if(serverOK) return;
 if(clientActive) return;
 document.getElementById('status').innerText='Server blocked on Render - Switching to CLIENT direct...';
 startClient();
}

function startClient(){
 clientActive=true;
 const url=ENDPOINTS[idx%3];
 document.getElementById('status').innerText='CLIENT direct Trying '+url.slice(8,22)+' #'+(idx+1);
 document.getElementById('log').innerText='Client attempt '+url;
 try{
  clientWS=new WebSocket(url);
  clientWS.onopen=()=>{document.getElementById('status').innerText='LIVE REAL CLIENT @ '+new Date().toLocaleTimeString()+' via '+url.slice(8,20); clientWS.send(JSON.stringify({ticks:cur,subscribe:1}));};
  clientWS.onmessage=(e)=>{
   const d=JSON.parse(e.data);
   if(d.tick && d.tick.symbol===cur){
     showPrice(d.tick.quote, d.tick.id, 'CLIENT '+url.slice(8,20));
     document.getElementById('status').innerText='LIVE REAL CLIENT @ '+new Date().toLocaleTimeString()+' via '+url.slice(8,20);
   }
  };
  clientWS.onerror=()=>{idx++; setTimeout(startClient,900);};
  clientWS.onclose=()=>{if(document.getElementById('price').innerText==='--'){idx++; setTimeout(startClient,900);} else {document.getElementById('status').innerText='Client closed - reconnect'; idx++; setTimeout(startClient,1500);}};
 }catch(e){idx++; setTimeout(startClient,900);}
}

setPair(cur);
setInterval(pollServer,900);
setTimeout(checkFailover,4000);
pollServer();
</script></body></html>
"""

@app.route('/')
def home(): return HTML

@app.route('/api/prices')
def prices(): return jsonify(PRICES)

@app.route('/health')
def health(): return "OK"
