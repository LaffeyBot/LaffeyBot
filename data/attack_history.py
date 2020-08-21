from datetime import datetime
from data.init_database import get_connection
from data.get_date_int import get_date_int, get_date_start_end
from data.model import *
from nonebot import get_bot
from typing import List


def get_list_of_attacks(date: datetime, group: Group) -> list:
    db.init_app(get_bot().server_app)
    start, end = get_date_start_end(date)

    players: List[User] = group.users.all()

    attack_times = dict()
    name: tuple
    for player in players:
        attack_times[player.nickname] = 0

    records: List[PersonalRecord] = PersonalRecord.query.filter_by(group_id=group.id) \
        .filter(PersonalRecord.detail_date >= start) \
        .filter(PersonalRecord.detail_date <= end)

    record_name: tuple
    for record in records:
        if record.nickname in attack_times:
            attack_times[record.nickname] += 1
        else:
            attack_times[record.nickname] = 1

    attack_times_list: list = list(attack_times.items())
    attack_times_list.sort(key=take_times, reverse=True)  # 根据伤害从高到低排列
    return attack_times_list


def take_times(e):
    return e[1]
