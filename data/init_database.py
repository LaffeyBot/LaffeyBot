import sqlite3


def init_database():
    connection = sqlite3.connect('main.db')
    connection.execute('CREATE TABLE IF NOT EXISTS record ('
                       'username TEXT NOT NULL,'
                       'target TEXT NOT NULL,'
                       'damage INTEGER DEFAULT 0,'
                       'date INTEGER NOT NULL'
                       ');')
    connection.execute('CREATE TABLE IF NOT EXISTS status ('
                       'key TEXT PRIMARY KEY,'
                       'value TEXT NOT NULL'
                       ');')
    connection.execute('CREATE TABLE IF NOT EXISTS player_list ('
                       'qq_name TEXT,'
                       'player_name TEXT'
                       ');')
    connection.commit()


def get_connection():
    return sqlite3.connect('main.db')


if __name__ == '__main__':
    init_database()
