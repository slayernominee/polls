import sqlite3

db = 'data/accounts.db'

# TODO: load all values in the response and load the matching permissions 
# TODO: create a new user with zero permissions 

def check(username: str, password_hash: str) -> dict:
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM accounts WHERE username=? AND password_hash=?', (username, password_hash))
        item = c.fetchone()
    
    if not item:
        return {
            "valid": False
        }
    
    return {
        "valid": True,
        "id": item[0]
    }