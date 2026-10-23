import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    html = """
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;background:#020617;color:white;padding:10px;margin:0}
.card{background:#0f172a;padding:18px;border-radius:20px;max-width:460px;margin:10px auto;border:1px solid #1e293b}
.live{color:#22c55e;font-weight:bold;font-size:12px}
.signal-box{border:1px solid #22c55e;background:#020617;padding:14px;border-radius:12px;margin:12px 0}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}
.stat{background:#1e293b;padding:16px;border-radius:12px;text-align:center;font-size:13px;line-height:1.6}
.btn{background:#3b82f6;color:white;padding:10px 14px;border-radius:8px;text-decoration:none;display:inline-block;margin:4px;font-size:13px}
.price{font-size:18px;font-weight:bold}
.real-badge{font-size:10px;padding:2px 6px;border-radius:10px;background:#22c55e;color:black}
</style>
</head>
<body>
<div class="card">
<h2 style="margin:0">🚀 Alufx ULTIMATE</h2>
<p class="live">● LIVE — REAL Deriv WS — No API Key</p>
<p style="font-size:11px;color:#94a3b8">Feed: wss://ws.binaryws.com — app_id 1089 — Direct Browser</p>

<div class="signal-box">
<div id="mainSig" style="color:#22c55e;font-weight:bold;font-size:20px">Connecting...</div>
<div style="font-size:12px;margin-top:6px;color:#cbd5e1" id="mainInfo">Waiting Real Tick...</div>
</div>

<h3 style="font-size:13px;margin:12px 0 8px 0;color:#f59e0b">🔥 REAL Prices: Vol 20 | GainX400 | Step 500/400</h3>
<div class="grid">
<div class="stat">
<div><span class="real-badge" id="b1">CONNECTING</span> Volatility 20</div>
<div class="price" id
