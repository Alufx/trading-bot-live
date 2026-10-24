from flask import Flask, jsonify, request
import random
from datetime import datetime

app = Flask(__name__)
LOG = []

def gen(pair):
    rsi = random.randint(22,78)
    acc = random.randint(82,92)
    price = round(1.05 + random.uniform(0.02,0.08),5)
    if "JPY" in pair: price = round(148 + random.uniform(-2,2),3)
    if "BTC" in pair: price = round(67400 + random.uniform(-500,500),2)
    if rsi < 38:
        d="CALL ▲"; c="#22c55e"; bg="#052e16"; tr="DOWN"; bb="LOWER"
    elif rsi > 65:
        d="PUT ▼"; c="#ef4444"; bg="#450a0a"; tr="UP"; bb="UPPER"
    else:
        d="WAIT ●"; c="#f59e0b"; bg="#451a03"; tr="RANGE"; bb="MIDDLE"
    return {"price":price,"dir":d,"color":c,"bg":bg,"rsi":rsi,"acc":acc,"trend":tr,"bb":bb}

@app.route('/')
def home():
    return """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>POCKET V3.1 FIX</title><style>
body{margin:0;background:#020617;color:#fff;font-family:system-ui} .app{max-width:420px;margin:0 auto;background:#0b1220;min-height:100vh;padding:12px;border:2px solid #2563eb;border-radius:20px}
.pairs{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:10px 0}
.pairs button{padding:10px 2px;border-radius:12px;border:0;background:#1e293b;color:#cbd5e1;font-weight:700;font-size:12px}
.pairs button.active{background:#e0f2fe;color:#0c4a6e}
.tf{display:flex;gap:6px;color:#64748b;font-size:13px;align-items:center;margin:8px 0}
.tf button{padding:8px 14px;border-radius:12px;border:0;background:#1e293b;color:#fff}
.tf button.active{background:#fff;color:#000;font-weight:900}
.price{text-align:center;font-size:48px;font-weight:900;margin:6px 0}
.sig{padding:18px;border-radius:16px;text-align:center;font-size:26px;font-weight:900;border:2px solid;margin:10px 0;background:#1e293b;color:#94a3b8}
.row{display:flex;justify-content:space-between;background:#151f32;padding:14px;border-radius:14px;margin:7px 0}
.btn{width:100%;padding:18px;border-radius:16px;border:0;font-weight:900;font-size:19px;background:linear-gradient(90deg,#38bdf8,#22c55e);color:#000}
.small{font-size:12px;color:#f59e0b;text-align:center;margin:8px 0}
.log{background:#020617;padding:8px;border-radius:10px;font-size:11px}
</style></head><body><div class=app>
<div style="display:flex;justify-content:space-between"><h2 style="margin:0">POCKET V3.1<br>FIX</h2><button id=modeBtn onclick="toggle()" style="padding:8px 18px;border-radius:20px;border:0;background:#3b82f6;color:#fff;font-weight:900">DEMO</button></div>
<div style="color:#22c55e;font-size:13px;margin:6px 0">● LIVE - Instant Signal - OTC</div>
<div class=pairs id=pairs></div>
<div class=tf>Timeframe:<button onclick="setTF('1m')" id=tf1m class=active>1m</button><button onclick="setTF('2m')" id=tf2m>2m</button><button onclick="setTF('5m')" id=tf5m>5m</button></div>
<div id=label style="text-align:center;color:#f59e0b;font-weight:900;font-size:18px">EURUSD_otc - 1m</div>
<div class=price id=price>1.09351</div>
<div class=sig id=sig>Click GET SIGNAL</div>
<div class=row><span>RSI</span><b id=rsi>--</b></div>
<div class=row><span>Accuracy</span><b id=acc>--%</b></div>
<div class=row><span>Trend</span><b id=trend>--</b></div>
<div class=row><span>BB</span><b id=bb>--</b></div>
<button class=btn onclick="getSig()">🔔 GET SIGNAL NOW</button>
<div class=small>Next candle in: <b id=timer>00:50</b> | <span id=modeTxt>DEMO</span></div>
<div style="font-size:13px;font-weight:700;margin-top:6px">History (Real+Demo same):</div><div class=log id=log></div>
</div>
<script>
let cur='EURUSD_otc',tf='1m',mode='DEMO';
const P=["EURUSD","GBPUSD","EURJPY","USDJPY","AUDUSD","EURGBP","GBPJPY","BTCUSD"];
function render(){let h='';P.forEach(p=>{let full=p+'_otc';if(p=='BTCUSD')full=p;let active=full.includes(cur)||p==cur.replace('_otc','');h+=`<button onclick="setPair('${full}')" id="p-${p}" class="${active?'active':''}">${p}</button>`});document.getElementById('pairs').innerHTML=h}
function setPair(p){if(!p.includes('_otc')&&p!='BTCUSD')p=p+'_otc';cur=p;render();document.getElementById('label').innerText=p+' - '+tf;document.getElementById('price').innerText=(1+Math.random()).toFixed(5)}
function setTF(t){tf=t;document.querySelectorAll('.tf button').forEach(b=>b.classList.remove('active'));document.getElementById('tf'+t).classList.add('active');document.getElementById('label').innerText=cur+' - '+t}
function toggle(){mode=mode=='DEMO'?'REAL':'DEMO';document.getElementById('modeBtn').innerText=mode;document.getElementById('modeBtn').style.background=mode=='REAL'?'#22c55e':'#3b82f6';document.getElementById('modeTxt').innerText=mode}
async function getSig(){let r=await fetch(`/api/signal?pair=${cur}&tf=${tf}`);let d=await r.json();
document.getElementById('price').innerText=d.price;document.getElementById('label').innerText=`${d.pair} - ${d.tf} - ${d.price}`;
let b=document.getElementById('sig');b.innerText=`${d.dir} ${d.pair.replace('_otc','')} ${d.acc}%`;b.style.color=d.color;b.style.borderColor=d.color;b.style.background=d.bg;
document.getElementById('rsi').innerText=d.rsi;document.getElementById('acc').innerText=d.acc+'%';document.getElementById('trend').innerText=d.trend;document.getElementById('bb').innerText=d.bb;
document.getElementById('log').innerHTML=d.log.map(x=>`<div>${x}</div>`).join('')}
render();
let s=50;setInterval(()=>{s--;if(s<0)s=59;document.getElementById('timer').innerText=`00:${String(s).padStart(2,'0')}`},1000);
</script></body></html>"""

@app.route('/api/signal')
def api():
    pair=request.args.get('pair','EURUSD_otc')
    tf=request.args.get('tf','1m')
    d=gen(pair)
    entry=f"{datetime.now().strftime('%H:%M:%S')} {pair} {tf} {d['dir']} {d['acc']}%"
    LOG.insert(0,entry)
    if len(LOG)>8: LOG.pop()
    return jsonify({"pair":pair,"tf":tf,"price":d["price"],"dir":d["dir"],"color":d["color"],"bg":d["bg"],"rsi":d["rsi"],"acc":d["acc"],"trend":d["trend"],"bb":d["bb"],"log":LOG})

@app.route('/health')
def h(): return "OK"
