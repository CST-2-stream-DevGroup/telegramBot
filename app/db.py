import sqlite3 as sq
from dataclasses import dataclass


async def db_start():
    database = sq.connect('new.db')
    cur = database.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS coord(user_id TEXT, lat TEXT, long TEXT )")
    database.commit()
    database.close()

async def create(user_id, lat, long):
    database = sq.connect('new.db')
    cur = database.cursor()
    cur.execute("INSERT INTO coord VALUES(?, ?, ?)", (user_id, lat, long))
    database.commit()
    database.close()

async def take_coords():
    database = sq.connect('new.db')
    cur = database.cursor()
    cur.execute("SELECT lat, long FROM coord")
    results = cur.fetchall()
    database.close()
    return results

