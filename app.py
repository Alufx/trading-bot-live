from flask import Flask, jsonify
app = Flask(__name__)
@app.route('/')
def home(): return "<h1>Alufx V4 GREEN OK - now add REAL</h1>"
@app.route('/health')
def h(): return "OK"
