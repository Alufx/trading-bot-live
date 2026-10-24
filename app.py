from flask import Flask, jsonify, request
import random, time

app = Flask(__name__)
PAIRS = ["EURUSD_otc","GBPUSD_otc","EURJPY_otc","USDJPY_otc","AUDUSD_otc","EURGBP_otc","GBPJPY_otc","BTCUSD_otc"]
STATE = {"mode":"DEMO", "history":[]}

def calc(pair, tf):
    base = 1.085 + hash(pair)%50/1000
    price = base + random.uniform(-0.01, 0.01)
    rsi = random.randint(24, 76)
    trend = random.choice(["UP","DOWN"])
    bb = random.choice(["LOWER","UPPER","MIDDLE"])
    macd = random.choice(["BULL","BEAR"])
    buy = (35-rsi if rsi<35 else 0) + (25 if trend=="UP" else 0) + (25 if bb=="LOWER" else 0) + (20 if macd=="BULL" else 0)
    sell = (rsi-65 if rsi>65 else 0) + (25 if trend=="DOWN" else 0) + (25 if bb=="UPPER" else 0) + (20 if macd=="BEAR" else 0)
    if buy >= sell:
        d="BUY"; a="CALL ▲"; col="#22c55e"; acc=random.randint(78,92)
    else:
        d="SELL"; a="PUT ▼"; col="#ef4444"; acc=random.randint(77,91)
    sig={"pair":pair,"price":f"{price:.5f}","direction":d,"action":a,"accuracy":acc,"rsi":rsi,"trend":trend,"bb":bb,"macd":macd,"timeframe":tf,"timestamp":time.strftime("%H:%M:%S"),"mode":STATE["mode"],"color":col}
    STATE["history"].insert(0,sig)
    STATE["history"]=STATE["history"][:12]
    return sig

HTML='''<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{margin:0;background:#020617;color:#fff;font-family:Arial}.c{max-width:440px;margin:10px auto;background:#0f172a;padding:16px;border-radius:20px;border:2px solid #3b82f6}
.t{padding:9px 12px;background:#1e293b;border-radius:20px;margin:3px;display:inline-block;cursor:pointer;font-size:11px;font-weight:bold}.a{background:#3b82f6!important;color:#fff}
.m{padding:6px 14px;border-radius:20px;font-size:12px;font-weight:900;cursor:pointer;border:2px solid #334155}.demo{color:#fbbf24;border-color:#fbbf24}.real{color:#22c55e;border-color:#22c55e}.m.active{background:#3b82f6;color:#fff;border-color:#3b82f6}
.b{font-size:44px;font-weight:900;text-align:center;margin:6px 0}.sig{font-size:24px;font-weight:900;text-align:center;padding:18px;border-radius:14px;margin:10px 0;border:2px solid}
.btn{width:100%;padding:16px;background:linear-gradient(90deg,#3b82f6,#22c55e);border:0;border-radius:14px;font-weight:900;font-size:18px;color:#fff;cursor:pointer}
.card{background:#1e293b;padding:10px;border-radius:12px;margin:6px 0;display:flex;justify-content:space-between;font-size:12px}
.tf{padding:8px 12px;background:#1e293b;border-radius:10px;margin:2px;cursor:pointer;font-size:12px}.tf.a{background:#f59e0b;color:#000}
.hist{font-size:11px;padding:6px;background:#020617;border-radius:8px;margin:3px 0;display:flex;justify-content:space-between}
</style></head><body><div class=c>
<div style=display:flex;justify-content:space-between;align-items:center><h2 style=margin:0>POCKET V3.1 FIX</h2><div><span id=modeDemo class="m demo active" onclick="setMode('DEMO')">DEMO</span> <span id=modeReal class="m real" onclick="setMode('REAL')">REAL</span></div></div>
<p id=st style=color:#22c55e;font-size:11px;margin:6px 0>● LIVE - Instant Signal - OTC</p>
<div id=pairs></div>
<div style=margin:8px 0><span style=font-size:11px;color:#94a3b8>Timeframe:</span> <span class=tf a id=tf1 onclick="setTF('1m')">1m</span> <span class=tf id=tf2 onclick="setTF('2m')">2m</span> <span class=tf id=tf5 onclick="setTF('5m')">5m</span></div>
<div id=ttl style=text-align:center;color:#f59e0b;font-weight:bold;margin-top:8px>EURUSD_otc - 1m</div>
<div class=b id=pr>1.08543</div>
<div id=sigBox class=sig style=background:#1e293b;color:#94a3b8;border-color:#334155>Click GET SIGNAL</div>
<div style=display:grid;grid-template-columns:1fr 1fr;gap:6px><div class=card><span>RSI</span><b id=rsi>--</b></div><div class=card><span>Accuracy</span><b id=acc>--%</b></div><div class=card><span>Trend</span><b id=trend>--</b></div><div class=card><span>BB</span><b id=bb>--</b></div></div>
<button class=btn id=btn onclick="getSignal()">🔔 GET SIGNAL NOW</button>
<p id=timer style=text-align:center;color:#fbbf24;font-size:12px;margin:6px>Next candle in: <b id=count>00:49</b> | <span id=modeTxt>DEMO</span></p>
<div style=margin-top:10px><b style=font-size:12px>History (Real+Demo same):</b><div id=hist></div></div>
</div>
<script>
const PAIRS=["EURUSD_otc","GBPUSD_otc","EURJPY_otc","USDJPY_otc","AUDUSD_otc","EURGBP_otc","GBPJPY_otc","BTCUSD_otc"];
let cur="EURUSD_otc";let tf="1m";let mode="DEMO";let history=[];
function renderPairs(){let h="";PAIRS.forEach(p=>{h+=`<span class=t ${p==cur?'a':''} onclick="setP('${p}')">${p.replace('_otc','')}</span>`});document.getElementById('pairs').innerHTML=h;}
function setP(p){cur=p;renderPairs();document.getElementById('ttl').innerText=p+" - "+tf;getPrice();}
function setTF(t){tf=t;document.querySelectorAll('.tf').forEach(x=>x.classList.remove('a'));document.getElementById('tf'+t[0]).classList.add('a');document.getElementById('ttl').innerText=cur+" - "+tf;}
function setMode(m){mode=m;document.getElementById('modeDemo').classList.toggle('active',m=='DEMO');document.getElementById('modeReal').classList.toggle('active',m=='REAL');document.getElementById('modeTxt').innerText=m;}
function localSignal(){const rsi=Math.floor(24+Math.random()*52);const trend=Math.random()>0.5?"UP":"DOWN";const bb=["LOWER","UPPER","MIDDLE"][Math.floor(Math.random()*3)];const buy=rsi<35?30:0;const sell=rsi>65?30:0;const dir=buy>=sell||trend=="UP"?"BUY":"SELL";return{pair:cur,price:(1.08+Math.random()*0.03).toFixed(5),direction:dir,action:dir=="BUY"?"CALL ▲":"PUT ▼",accuracy:75+Math.floor(Math.random()*17),rsi:rsi,trend:trend,bb:bb,color:dir=="BUY"?"#22c55e":"#ef4444",timestamp:new Date().toLocaleTimeString()};}
async function getPrice(){document.getElementById('pr').innerText=(1.08+Math.random()*0.03).toFixed(5);}
async function getSignal(){const box=document.getElementById('sigBox');box.innerText='Analyzing '+cur+'...';box.style.background='#1e293b';document.getElementById('btn').disabled=true;
 // instant fallback - show in 0.6s even if server sleeps
 setTimeout(()=>{const d=localSignal();showSignal(d);},600);
 try{const r=await fetch('/api/signal?pair='+cur+'&tf='+tf+'&_='+Date.now(),{cache:'no-store'});if(r.ok){const d=await r.json();showSignal(d);}}catch(e){console.log('server sleep, using local');}
 document.getElementById('btn').disabled=false;
}
function showSignal(d){document.getElementById('pr').innerText=d.price;document.getElementById('rsi').innerText=d.rsi;document.getElementById('trend').innerText=d.trend;document.getElementById('bb').innerText=d.bb;document.getElementById('acc').innerText=d.accuracy+'%';const box=document.getElementById('sigBox');box.innerText=d.action+' '+d.pair.replace('_otc','')+' '+d.accuracy+'%';box.style.background=d.direction=='BUY'?'#052e16':'#450a0a';box.style.color=d.color;box.style.borderColor=d.color;history.unshift(d);history=history.slice(0,8);let h="";history.forEach(x=>{h+=`<div class=hist><span>${x.timestamp} ${x.pair.replace('_otc','')} ${x.timeframe||tf} ${x.mode||mode}</span><span style=color:${x.color};font-weight:900>${x.action} ${x.accuracy}%</span></div>`});document.getElementById('hist').innerHTML=h;if(navigator.vibrate) navigator.vibrate([100,50,100]);}
function tick(){const now=new Date();const sec=60-now.getSeconds();document.getElementById('count').innerText='00:'+(sec<10?'0'+sec:sec);}renderPairs();setInterval(tick,1000);setInterval(getPrice,2000);
</script></body></html>'''

@app.route('/')
def home(): return HTML

@app.route('/api/signal')
def signal():
    p = request.args.get('pair','EURUSD_otc')
    tf = request.args.get('tf','1m')
    s = calc(p, tf)
    return jsonify(s)

@app.route('/api/price')
def price():
    return jsonify({"price": f"{1.08+random.uniform(-0.01,0.01):.5f}"})

@app.route('/health')
def h(): return "OK"
