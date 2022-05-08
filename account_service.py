import sqlite3

def get_balance(account_number, owner):
    try:
        con = sqlite3.connect('black_cat_market.db')
        cur = con.cursor()
        # Note: You can see that also specify exactly what it is that
        # we want from each query request because, it prevents malicious agents 
        # from getting everything related to the selected account
        cur.execute('''
            SELECT balance FROM account where id=? and owner=?''',
            (account_number, owner))
        row = cur.fetchone()
        # Note: By returning none, both when an account both does not exist, or is 
        #       not owned by the specified user, it ensures that hackers can't 
        #       perform user enumeration attacks to determine what account exist, 
        #       and what account don't
        if row is None:
            return None
        return row[0]
    finally:
        con.close()

def get_accounts(owner):
    print(owner)
    try:
        con = sqlite3.connect('black_cat_market.db')
        cur = con.cursor()
        cur.execute('''
            SELECT id FROM account where owner=?''',
            (owner,))
        row = cur.fetchall()
        result = []
        if len(row) == 0:
            return None
        for account in row:
            result.append(account[0])
        return result
    finally:
        con.close()

def do_transfer(source, target, amount):
    try:
        con = sqlite3.connect('black_cat_market.db')
        cur = con.cursor()
        cur.execute('''
            SELECT id FROM account where id=?''',
            (target,))
        row = cur.fetchone()
        if row is None:
            return False
        cur.execute('''
            UPDATE account SET balance=balance-? where id=?''',
            (amount, source))
        cur.execute('''
            UPDATE account SET balance=balance+? where id=?''',
            (amount, target))
        con.commit()
        return True
    finally:
        con.close()