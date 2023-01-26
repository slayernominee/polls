from flask import Flask, redirect, abort, session, request, render_template
from os import urandom
from controler import polls

app = Flask(__name__)
app.secret_key = str(urandom(4096))

wdata = {
    "footer": False
}

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('pages/index.html', wdata=wdata)

@app.route('/poll/<link>', methods=['GET', 'POST'])
def poll(link):
    poll = polls.get_by_link(link)
    return render_template('pages/poll.html', wdata=wdata, sheet=poll.sheet, title=poll.title, description=poll.description)

if __name__ == '__main__': 
    # debug run
    app.run(host='0.0.0.0', port=8080, debug=True)