from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Alufx REAL Deriv - WORKING</h1>
    <div id="p">Connecting...</div>
    <script>
    const ws = new WebSocket('wss://ws.binaryws.com/websockets/v3?app_id=1089');
    ws.onopen = () => ws.send(JSON.stringify({ticks:'R_20'}));
    ws.onmessage = (e) => {
      const d = JSON.parse(e.data);
      if(d.tick) document.getElementById('p').innerHTML = 'Vol 20 REAL: ' + d.tick.quote + ' LIVE @ ' + new Date().toLocaleTimeString();
    };
    </script>
    """
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
