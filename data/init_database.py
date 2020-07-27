import pymysql
import config
from functools import wraps
from quart import g


def init_database():
    connection = get_connection().cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS group_list ('
                       'group_id BIGINT NOT NULL '
                       ');')
    connection.execute('CREATE TABLE IF NOT EXISTS player_list ('
                       'group_id BIGINT NOT NULL,'
                       'qq_id BIGINT NOT NULL,'
                       'qq_name TEXT,'
                       'role TEXT,'
                       'password TEXT,'
                       'player_name TEXT,'
                       'id INT NOT NULL PRIMARY KEY AUTO_INCREMENT'
                       ');')
    connection.execute('CREATE TABLE IF NOT EXISTS record ('
                       'group_id BIGINT NOT NULL,'
                       'username TEXT NOT NULL,'
                       'target TEXT NOT NULL,'
                       'damage INTEGER DEFAULT 0,'
                       'date INTEGER NOT NULL,'
                       'id INT NOT NULL PRIMARY KEY AUTO_INCREMENT'
                       ');')
    connection.execute('CREATE TABLE IF NOT EXISTS picture_list ('
                       'file_name TEXT,'
                       'sub_directory TEXT,'
                       'origin TEXT '
                       ');')
    connection.execute('CREATE TABLE IF NOT EXISTS picture_quota ('
                       'qq_id BIGINT UNIQUE PRIMARY KEY,'
                       'count integer '
                       ');')
    # connection.execute('CREATE TABLE IF NOT EXISTS message_record ('
    #                    'qq_id integer,'
    #                    'date date'
    #                    ');')
    connection.execute('CREATE TABLE IF NOT EXISTS rank_record ('
                       'group_id BIGINT NOT NULL,'
                       'date INTEGER,'
                       'ranking INTEGER '
                       ');')
    connection.execute('CREATE TABLE IF NOT EXISTS api_keys ('
                       'group_id BIGINT NOT NULL,'
                       'qq_id BIGINT NOT NULL,'
                       'api_key TEXT NOT NULL '
                       ');')
    connection.close()


def get_connection():
    return pymysql.connect(config.DATABASE_PATH,
                           config.DATABASE_USERNAME,
                           config.DATABASE_PASSWORD,
                           config.DATABASE_NAME)


def db_connection_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.db = get_connection()
        return f(*args, **kwargs)

    return decorated_function


if __name__ == '__main__':
    init_database()
