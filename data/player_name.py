from data.init_database import get_connection


def qq_to_game_name(qq_name: str, group_id: int) -> str:
    c = get_connection()
    cursor = c.cursor()
    cursor.execute('SELECT player_name FROM player_list '
                   'WHERE qq_name=%s AND group_id=%s', (qq_name, group_id))
    matching_record = cursor.fetchone()
    if matching_record is None:
        return qq_name
    else:
        return matching_record[0]


def get_closest_player_name(name: str, group_id: int):
    cursor = get_connection().cursor()
    cursor.execute('SELECT player_name FROM player_list '
                   'WHERE group_id=%s', (group_id,))
    all_players = cursor.fetchall()
    all_players_list = list()
    for item in all_players:
        all_players_list.append([item[0], 0])

    for element in all_players_list:
        for letter in name:
            if letter in element[0]:
                element[1] += 1

    all_players_list.sort(key=sort_by_relevance, reverse=True)
    if all_players_list[0][1] == 0:
        return '不知道是谁'
    else:
        return all_players_list[0][0]


def sort_by_relevance(element):
    return element[1]
