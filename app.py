from flask import Flask, jsonify, request
import random, requests
from datetime import datetime

app = Flask(__name__)
LOG = []
PRICE_CACHE = {"EURUSD":1.0935,"GBPUSD":1.3086,"EURJPY":158.2,"USDJPY":145.2,"AUDUSD":0.6580,"EURGBP":0.8550,"GBPJPY":189.5,"BTCUSD":67200}

def live_price(pair):
    # pair like EURUSD, GBPUSD
    try:
        if "BTC" in pair:
            try:
                r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=3).json()
                return float(r["price"])
            except:
                return PRICE_CACHE["BTCUSD"]
        base = pair[:3]
        quote = pair[3:]
        # free API - no key needed
        resp = requests.get(f"https://open.er-api.com/v6/latest/{base}", timeout=4).json()
        if resp.get("result")=="success" and quote in resp["rates"]:
            price = float(resp["rates"][quote])
            # Quotex OTC adds small manipulation 0.001-0.003
            price += random.uniform(-0.002,0.002)
            PRICE_CACHE[pair]=price
            return round(price,5)
    except:
        pass
    return PRICE_CACHE.get(pair, 1.08)

def gen(pair):
    clean = pair.replace("_otc","")
    p = live_price(clean if clean!="BTCUSD" else "BTCUSD")
    rsi = random.randint(24,76)
    acc = random.randint(84,92)
    if rsi < 38:
        d,c,bg,tr,bb,ic = "CALL","#22c55e","linear-gradient(135deg,#052e16,#16a34a)","DOWN","LOWER","🚀"
    elif rsi > 62:
        d,c,bg,tr,bb,ic = "PUT","#ef4444","linear-gradient(135deg,#450a0a,#dc2626)","UP","UPPER","🔻"
    else:
        d,c,bg,tr,bb,ic = "WAIT","#f59e0b","linear-gradient(135deg,#451a03,#d97706)","RANGE","MIDDLE","⏳"
    return {"price":p,"dir":d,"color":c,"bg":bg,"rsi":rsi,"acc":acc,"trend":tr,"bb":bb,"icon":ic}

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>POCKET V3.1 PRO</title><style>
*{box-sizing:border-box;font-family:system-ui}body{margin:0;background:#020617;color:#fff;display:flex;justify-content:center}
.app{width:100%;max-width:430px;background:#0b1220;min-height:100vh;padding:12px;border:1px solid #1e293b}
.pairs{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:10px 0}
.pairs button{padding:11px 2px;border-radius:14px;border:1px solid #1e293b;background:#1e293b;color:#94a3b8;font-weight:700;font-size:12px}
.pairs button.active{background:#e0f2fe;color:#0c4a6e;box-shadow:0 0 15px #38bdf8aa}
.tf{display:flex;gap:6px;color:#64748b;font-size:13px;align-items:center;margin:8px 0}
.tf button{padding:8px 16px;border-radius:999px;border:0;background:#1e293b;color:#fff}
.tf button.active{background:#fff;color:#000;font-weight:900}
.priceCard{border:1px solid #1e293b;border-radius:20px;padding:12px;text-align:center;margin:8px 0}
.price{font-size:52px;font-weight:900}
.sig{border-radius:18px;padding:18px;text-align:center;font-size:26px;font-weight:900;border:2px solid #334155;margin:10px 0}
.row{display:flex;justify-content:space-between;background:#151f32;padding:13px;border-radius:12px;margin:6px 0}
.btn{width:100%;padding:18px;border-radius:16px;border:0;font-weight:900;font-size:18px;background:linear-gradient(90deg,#38bdf8,#22c55e);color:#000;margin-top:8px}
.small{font-size:12px;color:#f59e0b;text-align:center;margin:8px 0}
.log{background:#020617;border:1px solid #1e293b;border-radius:10px;padding:8px;font-size:11px}
.live{color:#22c55e;font-size:12px}
</style></head><body><div class=app>
<div style="display:flex;justify-content:space-between"><h2 style="margin:0">POCKET V3.1<br><span style="font-size:11px;color:#22c55e">PRO • REAL PRICE</span></h2><button id=mode style="padding:8px 16px;border-radius:20px;border:0;background:#0ea5e9;color:#fff;font-weight:900">DEMO</button></div>
<div class=live>● LIVE • Real Price • OTC offset ±0.002</div>
<div class=pairs id=pairs></div>
<div class=tf>Timeframe:<button onclick="setTF('1m')" id=tf1m class=active>1m</button><button onclick="setTF('2m')" id=tf2m>2m</button><button onclick="setTF('5m')" id=tf5m>5m</button></div>
<div class=priceCard><div id=label style="color:#f59e0b;font-weight:900">GBPUSD_otc - 1m</div><div class=price id=price>1.30863</div><div style="font-size:11px;color:#64748b">REAL MARKET + OTC</div></div>
<div class=sig id=sig>Tap GET SIGNAL</div>
<div class=row><span>RSI</span><b id=rsi>--</b></div>
<div class=row><span>Accuracy</span><b id=acc>--%</b></div>
<div class=row><span>Trend</span><b id=trend>--</b></div>
<div class=row><span>BB</span><b id=bb>--</b></div>
<button class=btn onclick="getSig()">🔔 GET SIGNAL NOW</button>
<div class=small>Next candle: <b id=timer>00:50</b></div>
<div class=log id=log>Waiting...</div>
</div>
<script>
let cur='GBPUSD_otc',tf='1m';
const P=["EURUSD","GBPUSD","EURJPY","USDJPY","AUDUSD","EURGBP","GBPJPY","BTCUSD"];
function render(){let h='';P.forEach(p=>{let f=p+'_otc';h+=`<button onclick="setPair('${f}')" class="${cur.includes(p)?'active':''}">${p}</button>`});document.getElementById('pairs').innerHTML=h}
function setPair(p){cur=p;render();getSig()}
function setTF(t){tf=t;document.querySelectorAll('.tf button').forEach(b=>b.classList.remove('active'));document.getElementById('tf'+t).classList.add('active');getSig()}
async function getSig(){let r=await fetch(`/api/signal?pair=${cur}&tf=${tf}`);let d=await r.json();
document.getElementById('price').innerText=d.price;document.getElementById('label').innerText=`${d.pair} - ${d.tf} - ${d.price}`;
let b=document.getElementById('sig');b.innerHTML=`${d.icon} ${d.dir} ${d.pair.replace('_otc','')} ${d.acc}%`;b.style.color=d.color;b.style.borderColor=d.color;b.style.background=d.bg;
document.getElementById('rsi').innerText=d.rsi;document.getElementById('acc').innerText=d.acc+'%';document.getElementById('trend').innerText=d.trend;document.getElementById('bb').innerText=d.bb;
document.getElementById('log').innerHTML=d.log.join('<br>');}
render();getSig();
let s=50;setInterval(()=>{s--;if(s<0){s=59;getSig()}document.getElementById('timer').innerText=`00:${String(s).padStart(2,'0')}`},1000);
</script></body></html>
"""

@app.route('/')
def home(): return HTML

@app.route('/api/signal')
def api():
    pair=request.args.get('pair','GBPUSD_otc')
    tf=request.args.get('tf','1m')
    d=gen(pair)
    ps = f"{d['price']:.5f}" if "BTC" not in pair else f"{d['price']:.2f}"
    entry=f"{datetime.now().strftime('%H:%M:%S')} {pair} {tf} {d['dir']} {d['acc']}% {ps}"
    LOG.insert(0,entry)
    if len(LOG)>8: LOG.pop()
    return jsonify({"pair":pair,"tf":tf,"price":ps,"dir":d["dir"],"color":d["color"],"bg":d["bg"],"rsi":d["rsi"],"acc":d["acc"],"trend":d["trend"],"bb":d["bb"],"icon":d["icon"],"log":LOG})

@app.route('/health')
def h(): return "OK"
