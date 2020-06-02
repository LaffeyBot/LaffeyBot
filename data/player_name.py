from data.init_database import get_connection


def qq_to_game_name(qq_name: str) -> str:
    c = get_connection()
    matching_record = c.execute('SELECT player_name FROM player_list WHERE qq_name=?', (qq_name,)).fetchone()
    if matching_record is None:
        return qq_name
    else:
        return matching_record[0]


def get_closest_player_name(name: str):
    all_players = get_connection().execute('SELECT player_name FROM player_list').fetchall()
    all_players_list = list()
    for item in all_players:
        all_players_list.append([item[0], 0])

    for element in all_players_list:
        for letter in name:
            if letter in element[0]:
                element[1] += 1

    all_players_list.sort(key=sort_by_relevance, reverse=True)
    return all_players_list[0][0]


def sort_by_relevance(element):
    return element[1]
