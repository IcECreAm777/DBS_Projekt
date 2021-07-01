# This file is a collection of all needed database queries and operations

import sqlite3

conn = sqlite3.connect('db/dbs_project.db')
cursor = conn.cursor()


# checks for existing tables and creates them if needed
def init():
    # checks for the Land Table (WIP)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Land'")
    # cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Test'")
    test = cursor.rowcount
    if cursor.rowcount < 1:
        cursor.execute('''CREATE TABLE Land 
                            (Code TEXT PRIMARY KEY NOT NULL,
                             Name TEXT NOT NULL);''')
