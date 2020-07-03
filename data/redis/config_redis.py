import redis as r


def connect(host='localhost', port=6379):
    pool = r.ConnectionPool(host=host, port=port, decode_responses=True)
    rd = r.Redis(connection_pool=pool)
    return rd
