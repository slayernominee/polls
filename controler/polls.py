import sqlite3
import json

db = 'data/polls.db'

class Poll():
    def __init__(self, id: int, creator: int, created: int, cookie_prot: bool, user_agent_prot: bool, ip_prot: bool, typ: int, sheet: str, link: str, title: str, description: str = '') -> None:
        self.id = id
        self.creator = creator
        self.created = created
        self.protection = {
            "cookie": cookie_prot,
            "user_agent": user_agent_prot,
            "ip": ip_prot
        }
        self.typ = typ
        self.sheet_name = sheet
        self.link = link
        self.title = title
        self.description = description

        if sheet.endswith('.md'): 
            with open(f'data/sheets/{sheet}', 'r') as f:
                self.sheet = f.read().replace('\n', '<br>')
                self.json = False
        elif sheet.endswith('.json'):
            with open(f'data/surveys/{sheet}', 'r') as f:
                self.sheet = json.load(f)
                self.json = True
    
    def __str__(self) -> str:
        return f'<poll object {self.id}>'

def beautify(poll_tuple: tuple) -> Poll:
    return Poll(poll_tuple[0], poll_tuple[1], poll_tuple[2], poll_tuple[3], poll_tuple[4], poll_tuple[5], poll_tuple[6], poll_tuple[7], poll_tuple[8], poll_tuple[9], poll_tuple[10])   

def jsonfy(poll: Poll) -> dict:
    return {
        "id": poll.id,
        "creator": poll.creator,
        "created": poll.created,
        "protection": poll.protection,
        "type": poll.typ,
        "sheet": poll.sheet,
        "link": poll.link,
        "title": poll.title,
        "description": poll.description
    }

def get_by_id(id: int) -> Poll:
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM polls WHERE id=?', (id, ))
        poll_tuple = c.fetchone()
    
    if poll_tuple:
        poll = beautify(poll_tuple)
        return poll

def get_by_link(link: str) -> Poll:
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM polls WHERE link=?', (link, ))
        poll_tuple = c.fetchone()
    
    if poll_tuple:
        poll = beautify(poll_tuple)
        return poll

def list_polls() -> list:
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM polls')
        poll_tuples = c.fetchall()
    poll_list = []
    for t in poll_tuples:
        poll = beautify(t)
        poll = jsonfy(poll)
        poll_list.append(poll)
    return poll_list

def create_poll(id: int, creator: int, created: int, cookie_prot: bool, user_agent_prot: bool, ip_prot: bool, typ: int, sheet: str, link: str, title: str, description: str = '') -> Poll:
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO polls VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (id, creator, created, cookie_prot, user_agent_prot, ip_prot, typ, sheet, link, title, description))
        conn.commit()
