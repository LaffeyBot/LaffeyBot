from data.init_database import get_connection


def qq_to_game_name(qq_name: str) -> str:
    c = get_connection()
    matching_record = c.execute('SELECT player_name FROM player_list WHERE qq_name=?', (qq_name,)).fetchone()
    if matching_record is None:
        return ''
    else:
        return matching_record[0]
