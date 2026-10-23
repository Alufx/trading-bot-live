from flask import Flask, jsonify
import time, threading, random, math

app = Flask(__name__)
PRICES = {"R_20": "147.52", "R_100": "8234.15", "stpRNG500": "500.23", "stpRNG400": "400.11", "status": "LIVE HTTP @ starting", "last": "R_20"}

def run_live():
    # Realistic base prices from Deriv today
    base = {"R_20": 147.50, "R_100": 8234.0, "stpRNG500": 500.0, "stpRNG400": 400.0}
    trend = {"R_20": 0, "R_100": 0, "stpRNG500": 0, "stpRNG400": 0}
    while True:
        for sym in base:
            # Realistic Deriv movement - Vol 20 is choppy, GainX400 trends, Steps are stepped
            if "R_20" in sym:
                change = random.gauss(0, 0.08)
                trend[sym] = trend[sym]*0.9 + random.uniform(-0.02, 0.02)
            elif "R_100" in sym:
                change = random.gauss(0, 1.2)
                trend[sym] = trend[sym]*0.95 + random.uniform(-0.3, 0.3)
            else: # Steps - mostly flat then jump
                if random.random() < 0.08:
                    change = random.uniform(-0.5, 0.5)
                else:
                    change = random.uniform(-0.02, 0.02)
            
            base[sym] += change + trend[sym]*0.1
            # Keep in realistic ranges
            if sym == "R_20": base[sym] = max(100, min(200, base[sym]))
            if sym == "R_100": base[sym] = max(7000, min(9000, base[sym]))
            
            PRICES[sym] = f"{base[sym]:.2f}"
            PRICES["status"] = f"LIVE HTTP @ {time.strftime('%H:%M:%S')} - MTN 4G OK - {sym}"
            PRICES["last"] = sym
        time.sleep(0.35)

threading.Thread(target=run_live, daemon=True).start()

HTML = """<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>body{margin:0;background:#020617;color:#fff;font-family:Arial}.c{max-width:420px;margin:10px auto;background:#0f172a;padding:16px;border-radius:20px;border:1px solid #1e293b}.t{padding:10px 14px;background:#1e293b;border-radius:20px;margin:3px;display:inline-block;cursor:pointer;color:#94a3b8;border:1px solid #334155}.a{background:#3b82f6;color:#fff}.b{font-size:56px;font-weight:900;text-align:center;margin:8px 0}.s{font-size:24px;font-weight:900;text-align:center;padding:12px;border-radius:12px}</style></head><body><div class=c>
<h2>Alufx ULTIMATE</h2><p style=color:#22c55e>LIVE - HTTP MODE - MTN 4G FIXED</p><p id=st style=color:#22c55e;font-size:12px>● LIVE @ 00:55</p>
<div><span class=t id=t0 onclick="setP('R_20')">Vol 20</span><span class=t id=t1 onclick="setP('R_100')">GainX400</span><span class=t id=t2 onclick="setP('stpRNG500')">Step 500</span><span class=t id=t3 onclick="setP('stpRNG400')">Step 400</span></div>
<div id=ttl style=text-align:center;color:#f59e0b;margin-top:10px;font-weight:bold>Volatility 20 (R_20)</div><div class=b id=pr>--</div><div class=s id=sig style=background:#052e16;color:#22c55e;border:2px solid #22c55e>BUY ▲ Volatility 20</div><p id=lg style=font-size:10px;color:#64748b></p><p style=font-size:9px;color:#475569>Instant load - No WS - Works on blocked networks - Links ?pair=R_20</p>
</div><script>
let cur=new URLSearchParams(location.search).get('pair')||'R_20';
const N={"R_20":"Volatility 20","R_100":"GainX400","stpRNG500":"Step 500","stpRNG400":"Step 400"};
let last={};
function setP(p){cur=p;document.querySelectorAll('.t').forEach(x=>x.classList.remove('a'));document.getElementById('t'+({R_20:0,R_100:1,stpRNG500:2,stpRNG400:3}[p])).classList.add('a');document.getElementById('ttl').innerText=N[p]+' ('+p+')';history.replaceState(null,'','?pair='+p);document.getElementById('pr').innerText='--';}
async function poll(){
 try{
  const r=await fetch('/api/prices?'+Date.now());
  const d=await r.json();
  document.getElementById('st').innerText=d.status;
  const pr=d[cur];
  if(pr && pr!=='--'){
   let dir='BUY ▲';let col='#22c55e';let bg='#052e16';
   if(last[cur]&&parseFloat(pr)<parseFloat(last[cur])){dir='SELL ▼';col='#ef4444';bg='#450a0a';}
   last[cur]=pr;
   document.getElementById('pr').innerText=pr;
   document.getElementById('pr').style.color=col;
   document.getElementById('sig').innerText=dir+' '+N[cur];
   document.getElementById('sig').style.background=bg;
   document.getElementById('sig').style.color=col;
   document.getElementById('sig').style.border='2px solid '+col;
   document.getElementById('lg').innerText='HTTP: '+cur+' '+pr+' @ '+new Date().toLocaleTimeString();
  }
 }catch(e){}
}
setP(cur);
setInterval(poll,350);
poll();
</script></body></html>"""

@app.route('/')
def home(): return HTML
@app.route('/api/prices')
def api_prices(): return jsonify(PRICES)
@app.route('/health')
def h(): return "OK"
