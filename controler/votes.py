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
        
def user_agent_allowed(poll: int, ip: str, operating_system: str, browser: str, version: str, darkmode: int, screen_width: int, screen_height: int, user_agent: str, only_by_ip_match: bool = True) -> bool:
    """check if the user agent was not found in the db 

    Args:
        poll (int): the poll id
        ip (str): client ip adress
        operating_system (str): user agent detected os
        browser (str): user agent detected browser
        version (str): user agent detected browser version
        darkmode (bool): _description_
        screen_width (int): _description_
        screen_height (int): _description_
        user_agent (str): the user agent string
        only_by_ip_match (bool, optional): if user agent and ip needs to match both. Defaults to True.

    Returns:
        bool: if the vote should be allowed after the check
    """
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        if only_by_ip_match:
            c.execute('SELECT * FROM votes WHERE poll=? AND operating_system=? AND browser=? AND version=? AND darkmode=? AND screen_width=? AND screen_height=? AND user_agent=? AND ip=?', (poll, operating_system, browser, version, darkmode, screen_width, screen_height, user_agent, ip)) # type: ignore
        else:
            c.execute('SELECT * FROM votes WHERE poll=? AND operating_system=? AND browser=? AND version=? AND darkmode=? AND screen_width=? AND screen_height=? AND user_agent=?', (poll, operating_system, browser, version, darkmode, screen_width, screen_height, user_agent)) # type: ignore
        items = c.fetchall()
    if items == []:
        return True
    else:
        return False
