import sqlite3
from passlib.hash import pbkdf2_sha256

con = sqlite3.connect('black_cat_market.db')
cur = con.cursor()
cur.execute('''
    CREATE TABLE account (
        id text primary key, owner text, balance integer,
        foreign key(owner) references users(codename))''')
cur.execute(
    "INSERT INTO account VALUES (?, ?, ?)",
    ('100', 'Harvester', 7500))
cur.execute(
    "INSERT INTO account VALUES (?, ?, ?)",
    ('939', 'Harvester', 500))
cur.execute(
    "INSERT INTO account VALUES (?, ?, ?)",
    ('850', 'ThePhilosopher', 200))
cur.execute(
    "INSERT INTO account VALUES (?, ?, ?)",
    ('666', 'Krazy4KatNip', 1000))
cur.execute(
    "INSERT INTO account VALUES (?, ?, ?)",
    ('969', 'MrSniffsAlot', 1000))
con.commit()
con.close()
