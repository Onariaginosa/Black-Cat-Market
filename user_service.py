import sqlite3
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256
from flask import request, g
import jwt

SECRET = 'bfg28y7efg238re7r6t32gfo23vfy7237yibdyo238do2v3'

def get_user_with_credentials(codename, password):
    try:
        con = sqlite3.connect('black_cat_market.db')
        cur = con.cursor()
        # Note: You can see that we use query parameters here instead of the
        #       typical string interpolation. This eliminates dangerous 
        #       characters like ' or ", preventing users from injection 
        #       possibly malicious code into your database! Because we use 
        #       query parameters, these quotations disappear from the 
        #       query string leaving it safe from SQL injection!
        cur.execute('''
            SELECT codename, name, password FROM users where codename=?''',
            (codename,))
        row = cur.fetchone()
        if row is None:
            return None
        codename, name, hash = row
        if not pbkdf2_sha256.verify(password, hash):
            return None
        return {"codename": codename, "name": name, "token": create_token(codename)}
    finally:
        con.close()

def logged_in():
    token = request.cookies.get('auth_token')
    try:
        data = jwt.decode(token, SECRET, algorithms=['HS256'])
        g.user = data['sub']
        return True
    except jwt.InvalidTokenError:
        return False

def create_token(codename):
    # Note that we set a reasonable time limit for the tokens to expire, so that
    # no one piggy backs off of a prior user's token
    now = datetime.utcnow()
    payload = {'sub': codename, 'iat': now, 'exp': now + timedelta(minutes=60)}
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return token