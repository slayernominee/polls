from flask import Flask, redirect, abort, session, request, render_template
from os import urandom, path
from controler import polls, accounts
import controler.votes
from json import load as jload, dump as jdump
import re
from ua_parser import user_agent_parser

"""
Errors

514 invalid link not secured
"""

app = Flask(__name__)
app.secret_key = str(urandom(4096))

wdata = {
    "footer": False,
    "rainbow_bg": False
}

def is_allowed_specific_char(string):
    """string should only contain numbers and ascii letters"""
    charRe = re.compile(r'[^a-zA-Z0-9]')
    string = charRe.search(string)
    return not bool(string)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('pages/index.html', wdata=wdata)

@app.route('/poll/<link>', methods=['GET'])
def poll(link):
    poll = polls.get_by_link(link)
    if poll.typ == 1:
        return render_template('pages/qbq.html', wdata=wdata, sheet=poll.sheet, title=poll.title, description=poll.description, id=poll.id)
    else:
        return render_template('pages/poll.html', wdata=wdata, sheet=poll.sheet, title=poll.title, description=poll.description, id=poll.id)

@app.route('/admin')
def admin():
    if 'permissions' in session and 'admin' in session['permissions'] and session['permissions']['admin']:
        poll_list = polls.list_polls()
        account_list = accounts.list_accounts()
        return render_template('pages/admin.html', wdata=wdata, poll_list=poll_list, account_list=account_list)
    else:
        return render_template('pages/login.html', wdata=wdata)

@app.route('/login', methods=['POST'])
def admin_login():    
    form = request.form
    username = str(form['username'])
    password = str(form['password'])

    rs = accounts.check(username, password) # will be hashed with bcrypt and then checked

    if rs['valid']:
        if 'permissions' not in session:
            session['permissions'] = {}
        session['permissions'] = rs['permissions']
        return redirect('/admin')
    else:
        return abort(403)
        

@app.route('/poll/<link>', methods=['POST'])
def poll_post(link):
    if not is_allowed_specific_char(link):
        return abort(514)

    poll = polls.get_by_link(link)
    with open(f'data/surveys/{poll.id}.json', 'r') as f:
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
            if poll.result_hidden and not ('permissions' in session and 'admin' in session['permissions'] and session['permissions']['admin']):
                return 'disabled to see the results currently, but you cant vote again because double voting is disabled'
            return render_template('pages/poll_result.html', votes=votes, wdata=wdata, already_voted=True, title=poll.title, description=poll.description)
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
        if key.startswith('ans_'):
            question_id = int(key.split('_')[1])
            element_id = int(key.split('_')[2])
            option = form[key]
            votes['questions'][question_id]['elements'][element_id]['options'][option] += 1
    
    ua_string = request.user_agent.string
    parsed_ua = user_agent_parser.Parse(ua_string)
    version = parsed_ua['user_agent']['major'] + '.' + parsed_ua['user_agent']['minor'] + '.' + parsed_ua['user_agent']['patch'] # type: ignore
    controler.votes.vote_done(poll.id, str(request.remote_addr), str(parsed_ua['os']['family']), str(parsed_ua['user_agent']['family']), version, -1, -1, -1, ua_string) # type: ignore

    with open(f'data/surveys/{poll.id}.json', 'w') as f:
        jdump(votes, f, indent=2)

    return redirect(f'/poll/result/{link}')

@app.route('/poll/result/<link>')
def poll_result(link):

    if not is_allowed_specific_char(link):
        return abort(514)

    poll = polls.get_by_link(link)

    if poll == None:
        return 'no poll found ...'

    if poll.result_hidden and not ('permissions' in session and 'admin' in session['permissions'] and session['permissions']['admin']):
        return render_template('pages/poll_result_disabled.html', wdata=wdata, title=poll.title)

    with open(f'data/surveys/{poll.id}.json', 'r') as f:
        votes = jload(f)

    return render_template('pages/poll_result.html', wdata=wdata, votes=votes, title=poll.title, description=poll.description)

if __name__ == '__main__': 
    # debug run
    app.run(host='127.0.0.1', port=8080, debug=True)