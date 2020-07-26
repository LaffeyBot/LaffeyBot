from data.init_database import get_connection


def validate_api_key(api_key: str, group_id: str) -> bool:
    c = get_connection()
    cursor = c.cursor()
    matching: int = cursor.execute('SELECT * FROM api_keys '
                                   'WHERE group_id=%s AND api_key=%s',
                                   (group_id, api_key))
    return bool(matching)
