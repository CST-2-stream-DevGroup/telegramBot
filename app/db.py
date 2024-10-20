import sqlite3 as sq
from dataclasses import dataclass
from types import NoneType


async def db_start():
    database = sq.connect('new.db')
    cur = database.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS coord(user_id TEXT, lat TEXT,"
                " long TEXT, img TEXT, desc TEXT)")
    database.commit()
    database.close()


async def create(user_id, lat, long, img, desc):
    database = sq.connect('new.db')
    cur = database.cursor()
    cur.execute("INSERT INTO coord VALUES(?, ?, ?, ?, ?)",
                (user_id, lat, long, img, desc))
    database.commit()
    database.close()


async def take_coords():
    database = sq.connect('new.db')
    cur = database.cursor()
    cur.execute("SELECT lat, long FROM coord")
    results = cur.fetchall()
    database.close()
    return results


async def check_coords(lt, ln):
    database = sq.connect('new.db')
    cur = database.cursor()
    cur.execute("SELECT lat, long FROM coord")
    coords = cur.fetchall()
    print(coords)
    count = 0
    for i in range(len(coords)):
        if ((str(round(float(coords[i][0]), 4))[:5] == str(round(float(lt), 4))[:5]) or
                (str(round(float(coords[i][1]), 4))[:5] == str(round(float(ln), 4))[:5])):
            count += 1
    database.close()
    return True if count == 0 else False


async def take_inf(lt, ln):
    database = sq.connect('new.db')
    cur = database.cursor()
    cur.execute(f"SELECT img, desc FROM coord WHERE lat = {lt} and long = {ln}")
    results = cur.fetchall()
    database.close()
    return results
