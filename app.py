from flask import Flask, redirect, abort, session, request, render_template
from os import urandom

app = Flask(__name__)
app.secret_key = str(urandom(4096))

wdata = {}

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('pages/index.html', wdata=wdata)

if __name__ == '__main__': 
    # debug run
    app.run(host='0.0.0.0', port=8080, debug=True)