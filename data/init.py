import sqlite3


def init_database():
    connection = sqlite3.connect('main.db')
    connection.execute('CREATE TABLE [IF NOT EXISTS] record ('
                       'username TEXT NOT NULL,'
                       'target TEXT NOT NULL,'
                       'damage INTEGER DEFAULT 0'
                       ');')
    connection.execute('CREATE TABLE [IF NOT EXISTS] status ('
                       'key TEXT PRIMARY,'
                       'value TEXT NOT NULL,'
                       ');')
    connection.execute('CREATE TABLE [IF NOT EXISTS] player_list ('
                       'username TEXT UNIQUE,'
                       ');')




def get_connection():
    return sqlite3.connect('main.db')

