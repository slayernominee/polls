import sqlite3

db = 'data/votes.db'

def vote_done(poll: int, ip: str, operating_system: str, browser: str, version: str, darkmode: int, screen_width: int, screen_height: int, user_agent: str) -> None:
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute('SELECT MAX(id) FROM votes;')
        max_id = c.fetchone()
        if max_id[0] == None:
            max_id = -1
        else:
            max_id = max_id[0]
        id = max_id + 1
        c.execute('INSERT INTO votes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, poll, ip, operating_system, browser, version, darkmode, screen_width, screen_height, user_agent))
        conn.commit()