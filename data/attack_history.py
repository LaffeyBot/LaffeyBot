from datetime import datetime
from data.init_database import get_connection
from data.get_date_int import get_date_int


def get_list_of_attacks(date: datetime, group_id: int) -> list:
    c = get_connection()
    cursor = c.cursor()
    cursor.execute('SELECT player_name FROM player_list WHERE group_id=%s',
                   (group_id,))
    player_list = cursor.fetchall()

    attack_times = dict()
    name: tuple
    for name in player_list:
        attack_times[name[0]] = 0

    today = get_date_int(date)
    cursor.execute('SELECT username FROM record '
                   'WHERE date=%s AND group_id=%s', (today, group_id))
    attack_record = cursor.fetchall()

    record_name: tuple
    for record_name in attack_record:
        if record_name[0] in attack_times:
            attack_times[record_name[0]] += 1
        else:
            attack_times[record_name[0]] = 1

    attack_times_list: list = list(attack_times.items())
    attack_times_list.sort(key=take_times, reverse=True)  # 根据伤害从高到低排列
    return attack_times_list


def take_times(e):
    return e[1]
