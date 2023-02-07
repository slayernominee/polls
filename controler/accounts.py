import sqlite3
import bcrypt
import time

db = 'data/accounts.db'

def jsonfy(item: tuple) -> dict:
    return {
        "id": item[0],
        "username": item[1],
        "mail": item[2],

        "totp": item[4],
        "created": item[5]
    }

def list_accounts() -> list[dict]:
    with sqlite3.connect(db) as conn:
        account_list = []
        c = conn.cursor()
        c.execute('SELECT * FROM accounts')
        items = c.fetchall()
        for item in items:
            acc = jsonfy(item)
            account_list.append(acc)
    
    return account_list

def check(username: str, password: str) -> dict:
    b_password = password.encode('utf-8')
    salt = b'$2b$12$joWb2D.n3oRReP.s0fRxuO'
    b_password_hash = bcrypt.hashpw(b_password, salt)
    password_hash = b_password_hash.decode('utf-8')

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

# todo: create a new user
# + id generator
# + check if username & mail are free
# + give the user account an zero perm entry in the permissions db
def create(username: str, mail: str, password_hash: str, totp: str = '', created: float = time.time()):
    pass