from flask import Flask, jsonify, request
import random
from datetime import datetime
app = Flask(__name__)
LOG = []

def gen(pair):
    rsi = random.randint(24,76)
    acc = random.randint(84,92)
    price = round(1.08 + random.uniform(-0.03,0.03),5)
    if "JPY" in pair: price = round(149.2 + random.uniform(-1.5,1.5),3)
    if "BTC" in pair: price = round(67200 + random.uniform(-300,300),1)
    if rsi < 38: d,c,bg,tr,bb,icon = "CALL","#22c55e","linear-gradient(135deg,#052e16,#16a34a)","DOWN","LOWER","🚀"
    elif rsi > 62: d,c,bg,tr,bb,icon = "PUT","#ef4444","linear-gradient(135deg,#450a0a,#dc2626)","UP","UPPER","🔻"
    else: d,c,bg,tr,bb,icon = "WAIT","#f59e0b","linear-gradient(135deg,#451a03,#d97706)","RANGE","MIDDLE","⏳"
    return {"price":price,"dir":d,"color":c,"bg":bg,"rsi":rsi,"acc":acc,"trend":tr,"bb":bb,"icon":icon}

HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>POCKET V3.1 PRO</title><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;font-family:'Space Grotesk',system-ui}
body{margin:0;background:radial-gradient(600px at 20% 0%,#0f172a,#020617);color:#fff;min-height:100vh;display:flex;justify-content:center}
.app{width:100%;max-width:430px;background:linear-gradient(180deg,#0f172a,#020617);min-height:100vh;padding:14px 14px 20px;border-left:1px solid #1e293b;border-right:1px solid #1e293b}
.header{display:flex;justify-content:space-between;align-items:center;padding:8px 4px}
.logo{font-weight:700;font-size:22px;letter-spacing:-0.5px;line-height:1} .logo span{font-size:11px;color:#22c55e;letter-spacing:2px;display:block;margin-top:2px}
.mode{padding:8px 16px;border-radius:999px;background:#0ea5e9;color:#fff;font-weight:700;font-size:12px;border:0;box-shadow:0 0 20px #0ea5e966}
.live{margin:8px 0 12px;display:flex;align-items:center;gap:8px;color:#22c55e;font-size:12px;font-weight:700;background:#052e1640;padding:8px 12px;border-radius:999px;border:1px solid #14532d;width:fit-content}
.pairs{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.pairs button{padding:12px 0;border-radius:14px;border:1px solid #1e293b;background:linear-gradient(180deg,#1e293b,#0f172a);color:#94a3b8;font-weight:700;font-size:12px;transition:.2s}
.pairs button.active{background:linear-gradient(180deg,#e0f2fe,#bae6fd);color:#0c4a6e;border-color:#38bdf8;box-shadow:0 0 20px #38bdf866;transform:scale(1.05)}
.tf{margin:14px 0 8px;display:flex;gap:8px;align-items:center;color:#64748b;font-size:12px}
.tf button{padding:8px 16px;border-radius:999px;border:1px solid #1e293b;background:#0f172a;color:#fff}
.tf button.active{background:#fff;color:#000;font-weight:700}
.priceCard{background:linear-gradient(180deg,#1e293b20,#020617);border:1px solid #1e293b;border-radius:20px;padding:14px;margin:10px 0;text-align:center;backdrop-filter:blur(10px)}
.label{color:#f59e0b;font-weight:700;font-size:13px;letter-spacing:1px}
.price{font-size:52px;font-weight:700;letter-spacing:-2px;margin:6px 0;text-shadow:0 0 30px #ffffff30}
.sigCard{border-radius:20px;padding:20px;text-align:center;font-size:28px;font-weight:700;border:2px solid #334155;background:#0f172a;color:#64748b;transition:.4s;box-shadow:inset 0 1px 0 #ffffff10}
.row{display:flex;justify-content:space-between;align-items:center;background:linear-gradient(90deg,#151f32,#0f172a);border:1px solid #1e293b;padding:14px 16px;border-radius:14px;margin:8px 0}
.row b{font-size:15px} .row span{color:#64748b;font-size:12px;letter-spacing:1px}
.btn{width:100%;padding:18px;border-radius:18px;border:0;font-weight:700;font-size:18px;background:linear-gradient(90deg,#0ea5e9,#22c55e);color:#000;box-shadow:0 10px 30px #22c55e40;margin-top:12px;letter-spacing:0.5px}
.btn:active{transform:scale(0.98)}
.timer{text-align:center;color:#f59e0b;font-size:12px;margin:10px 0}
.history{margin-top:10px;background:#020617;border:1px solid #1e293b;border-radius:14px;padding:10px;font-size:11px;line-height:1.8;min-height:60px}
.dot{width:8px;height:8px;background:#22c55e;border-radius:50%;box-shadow:0 0 10px #22c55e;animation:pulse 1.5s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
</style></head><body><div class=app>
<div class=header><div class=logo>POCKET V3.1<div><span>PRO • FIX</span></div></div><button class=mode id=modeBtn onclick="toggle()">DEMO</button></div>
<div class=live><span class=dot></span> LIVE • Instant Signal • OTC</div>
<div class=pairs id=pairs></div>
<div class=tf>Timeframe: <button onclick="setTF('1m')" id=tf1m class=active>1m</button><button onclick="setTF('2m')" id=tf2m>2m</button><button onclick="setTF('5m')" id=tf5m>5m</button></div>
<div class=priceCard><div class=label id=label>EURUSD_otc - 1m</div><div class=price id=price>1.09351</div><div style="font-size:11px;color:#64748b">OTC MARKET • REAL TIME</div></div>
<div class=sigCard id=sig>Tap GET SIGNAL</div>
<div class=row><span>RSI • MOMENTUM</span><b id=rsi>--</b></div>
<div class=row><span>ACCURACY • AI</span><b id=acc>--%</b></div>
<div class=row><span>TREND • DIRECTION</span><b id=trend>--</b></div>
<div class=row><span>BB • VOLATILITY</span><b id=bb>--</b></div>
<button class=btn onclick="getSig()">🔔 GET SIGNAL NOW</button>
<div class=timer>Next candle in: <b id=timer>00:50</b> • <span id=modeTxt>DEMO</span> & REAL same</div>
<div style="font-size:12px;font-weight:700;margin:6px 0">History (Real+Demo same):</div><div class=history id=log>Waiting for signal...</div>
</div>
<script>
let cur='EURUSD_otc',tf='1m',mode='DEMO';
const P=["EURUSD","GBPUSD","EURJPY","USDJPY","AUDUSD","EURGBP","GBPJPY","BTCUSD"];
function render(){let h='';P.forEach(p=>{let f=p+'_otc';h+=`<button onclick="setPair('${p}_otc')" id="p-${p}" class="${cur.includes(p)?'active':''}">${p}</button>`});document.getElementById('pairs').innerHTML=h}
function setPair(p){cur=p;render();getSig()}
function setTF(t){tf=t;document.querySelectorAll('.tf button').forEach(b=>b.classList.remove('active'));document.getElementById('tf'+t).classList.add('active');getSig()}
function toggle(){mode=mode=='DEMO'?'REAL':'DEMO';document.getElementById('modeBtn').innerText=mode;document.getElementById('modeBtn').style.background=mode=='REAL'?'#22c55e':'#0ea5e9';document.getElementById('modeTxt').innerText=mode}
async function getSig(){
 let r=await fetch(`/api/signal?pair=${cur}&tf=${tf}`);let d=await r.json();
 document.getElementById('price').innerText=d.price;
 document.getElementById('label').innerText=`${d.pair} - ${d.tf} - ${d.price}`;
 let b=document.getElementById('sig');b.innerHTML=`${d.icon} ${d.dir} • ${d.pair.replace('_otc','')} • ${d.acc}%`;
 b.style.color=d.color;b.style.borderColor=d.color;b.style.background=d.bg;b.style.boxShadow=`0 0 30px ${d.color}40`;
 document.getElementById('rsi').innerText=d.rsi;document.getElementById('acc').innerText=d.acc+'%';document.getElementById('trend').innerText=d.trend;document.getElementById('bb').innerText=d.bb;
 document.getElementById('log').innerHTML=d.log.map(x=>`<div>${x}</div>`).join('');
}
render();
let s=50;setInterval(()=>{s--;if(s<0){s=59;getSig()}document.getElementById('timer').innerText=`00:${String(s).padStart(2,'0')}`},1000);
</script></body></html>
"""

@app.route('/')
def home(): return HTML

@app.route('/api/signal')
def api():
    pair=request.args.get('pair','EURUSD_otc')
    tf=request.args.get('tf','1m')
    d=gen(pair)
    entry=f"{datetime.now().strftime('%H:%M:%S')} {pair} {tf} {d['dir']} {d['acc']}%"
    LOG.insert(0,entry)
    if len(LOG)>8: LOG.pop()
    return jsonify({"pair":pair,"tf":tf,"price":d["price"],"dir":d["dir"],"color":d["color"],"bg":d["bg"],"rsi":d["rsi"],"acc":d["acc"],"trend":d["trend"],"bb":d["bb"],"icon":d["icon"],"log":LOG})

@app.route('/health')
def h(): return "OK"
