from flask import Flask, redirect, abort, session, request, render_template
from os import urandom
from controler import polls
from json import load as jload, dump as jdump

app = Flask(__name__)
app.secret_key = str(urandom(4096))

wdata = {
    "footer": False
}

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('pages/index.html', wdata=wdata)

@app.route('/poll/<link>', methods=['GET'])
def poll(link):
    poll = polls.get_by_link(link)
    return render_template('pages/poll.html', wdata=wdata, sheet=poll.sheet, title=poll.title, description=poll.description, id=poll.id)

@app.route('/poll/<link>', methods=['POST'])
def poll_post(link):
    poll = polls.get_by_link(link)
    
    with open(f'data/votes/{poll.id}.json', 'r') as f:
        votes = jload(f)

    protection = poll.protection
    
    # cookie protection
    if bool(protection['cookie']):
        # generate the session if not already created
        if 'votes' not in session:
            session['votes'] = {}
        if str(link) not in session['votes']:
            session['votes'][str(link)] = True
        # check if vote is allowed
        if not session['votes'][str(link)]:
            return render_template('pages/poll_result.html', votes=votes, wdata=wdata, already_voted=True)
        # write the cookie after vote
        session['votes'][str(link)] = False

    """
    TODO:
    ip protection
    user agent protection

    - check if user agent votes are protected
    - check if ip votes are protected

    - write ip in db for this link
    - block ip if found in the db

    - write user agent in the db
    - block if user agent found in db
    """

    form = request.form
    for key in form:
        value = form[key]
        if key.startswith('text_'):
            question = key.split('text_')[1]
        elif key.startswith('radio_'):
            question = key.split('radio_')[1]
        elif key == 'id':
            continue
        if question not in votes:
            votes[question] = {}
        
        if value not in votes[question]:
            votes[question][value] = 0
        votes[question][value] += 1
    
    with open(f'data/votes/{poll.id}.json', 'w') as f:
        jdump(votes, f, indent=2)
    return render_template('pages/poll_result.html', wdata=wdata, votes=votes)

if __name__ == '__main__': 
    # debug run
    app.run(host='0.0.0.0', port=8080, debug=True)