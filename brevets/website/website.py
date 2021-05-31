from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/list')
def list():
    data = request.args.get("csv", type=str, default="json")
    k = request.args.get("k", type=int, default=0)
    list_ = request.args.get("list", type=str)
    r = requests.get('http://restapi:5000/' + list_ + data + '?top=' + str(k))
    return r.text


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
