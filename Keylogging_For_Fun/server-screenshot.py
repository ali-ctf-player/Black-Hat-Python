

from flask import Flask,request

app = Flask(__name__)

@app.route('/upload',methods=['POST'])

def upload():

    if 'file' in request.files:
        file = request.files('file')
        file.save(f"received_{file.filename}")
        return "OK",200
    return "NO File" ,400


if __name__ == "__main__":
    app.run(host="192.168.100.14",port=5000)