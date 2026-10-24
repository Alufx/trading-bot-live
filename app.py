from flask import Flask, jsonify, request
import random
from datetime import datetime

app = Flask(__name__)

PAIRS = ["EURUSD_otc","GBPUSD_otc","EURJPY_otc","USDJPY_otc","AUDUSD_otc","EURGBP_otc","GBPJPY_otc","BTCUSD_otc"]
LOG = []

def gen(pair, tf):
    price = round(1.07 + random.uniform(-0.03,0.03),5)
    if "JPY" in pair: price = round(148.5 + random.uniform(-2,2),3)
    if "BTC" in pair: price = round(68000 + random.uniform(-400,400),1)
    rsi = random.randint(22,78)
    acc = random.randint(82,91)
    if rsi < 38:
        d, c, bg, trend, bb = "CALL ▲", "#22c55e", "#052e16", "DOWN", "LOWER"
    elif rsi > 62:
        d, c, bg, trend, bb = "PUT ▼", "#ef4444", "#450a0a", "UP", "UPPER"
    else:
        d, c, bg, trend, bb = "WAIT ●", "#f59e0b", "#451a03", "RANGE", "MIDDLE"
    return {"pair":pair,"price":price,"dir":d,"color":c,"bg":bg,"rsi":rsi,"acc":acc,"trend":trend,"bb":bb,"time":datetime.now().strftime("%H:%M:%S"),"tf":tf}

HTML = """<!DOCTYPE html>
<html><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#020617">
<title>POCKET V3.1 FIX</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#020617;color:#fff;font-family:system-ui}
.app{max-width:420px;margin:0 auto;background:#0b1220;min-height:100vh;padding:12px}
.pairs{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:10px 0}
.pairs button{padding:9px 2px;border-radius:10px;border:1px solid #1e293b;background:#1e293b;color:#94a3b8;font-size:11px;font-weight:800}
.pairs button.active{background:#e0f2fe;color:#0c4a6e;border-color:#38bdf8}
.tf{display:flex;gap:6px;align-items:center;color:#64748b;font-size:13
