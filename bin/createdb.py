import sqlite3
from passlib.hash import pbkdf2_sha256

con = sqlite3.connect('black_cat_market.db')
cur = con.cursor()
cur.execute('''
    CREATE TABLE users (
        codename text primary key, name text, password text)''')
cur.execute(
    "INSERT INTO users VALUES (?, ?, ?)",
    ('Harvester', 'Demeter', pbkdf2_sha256.hash("123456")))
cur.execute(
    "INSERT INTO users VALUES (?, ?, ?)",
    ('ThePhilosopher', 'Plato', pbkdf2_sha256.hash("123456")))
cur.execute(
    "INSERT INTO users VALUES (?, ?, ?)",
    ('MrSniffsAlot', 'Rum Tum Tugger', pbkdf2_sha256.hash("123456")))
cur.execute(
    "INSERT INTO users VALUES (?, ?, ?)",
    ('Krazy4KatNip', 'Macavity', pbkdf2_sha256.hash("123456")))
con.commit()
con.close()

