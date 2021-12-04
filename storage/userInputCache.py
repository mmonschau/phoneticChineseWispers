# coding=utf-8

import sqlite3 as sql

__DBCON__ = None


def create_DB(debug=False):
    global __DBCON__
    if __DBCON__ is None:
        conn = None
        if debug:
            conn = sql.connect('tmp.db', check_same_thread=False)
        else:
            conn = sql.connect(':memory:', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `userinput` (`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,	`token`	TEXT NOT NULL,	`number`	INTEGER NOT NULL, `uuid` TEXT NOT NULL ,	`input`	TEXT NOT NULL, `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `tokens` (	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,	`token`	TEXT UNIQUE, `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
        conn.commit()
        conn.row_factory = sql.Row
        __DBCON__ = conn
    return conn


def insert_token(token):
    __DBCON__.execute("INSERT INTO tokens(token) VALUES( :token)", {'token': token})
    __DBCON__.commit()


def get_tokens():
    conn = __DBCON__
    cursor = conn.cursor()
    cursor.execute("SELECT token, `timestamp` FROM tokens")
    tokens = cursor.fetchall()
    tokens = list(map(lambda x: dict(x),tokens))#convert to list
    #print(tokens)
    #return list(map(lambda x: x['token'], tokens))
    return tokens


def insert_user_entry(uuid, token, row_number, user_input):
    __DBCON__.execute("INSERT INTO userinput(uuid, token,number,input) VALUES(:uuid, :token,:number,:input)",
                      {'uuid': uuid, 'token': token, 'number': row_number, 'input': user_input})
    __DBCON__.commit()


def get_user_entries_by_token(token):
    conn = __DBCON__
    cursor = conn.cursor()
    cursor.execute("SELECT number, input, uuid FROM userinput WHERE token=:token ORDER BY id", {'token': token})
    entries = cursor.fetchall()
    return list(map(lambda x: dict(x), entries))
