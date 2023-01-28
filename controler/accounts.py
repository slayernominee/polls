import sqlite3

db = 'data/accounts.db'

# TODO: load all values in the response and load the matching permissions 
# TODO: create a new user with zero permissions 

def check(username: str, password_hash: str) -> dict:
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM accounts WHERE username=? AND password_hash=?', (username, password_hash))
        item = c.fetchone()
        if item:
            c.execute('SELECT * FROM permissions WHERE id=?', (item[0], ))
            perms_item = c.fetchone()
        else:
            perms_item = None
    
    if not item:
        return {
            "valid": False,
            "permissions": {}
        }
    
    if perms_item:
        permissions = {
            "admin": perms_item[1],
            "moderator": perms_item[2],
            "creator": perms_item[3]
        }
    else:
        permissions = {
            "admin": False,
            "moderator": False,
            "creator": False
        }

    return {
        "valid": True,
        "id": item[0],
        "permissions": permissions
    }