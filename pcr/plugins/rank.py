from nonebot import on_command, CommandSession
from data.init_database import get_connection
import config
from datetime import datetime
from data.player_name import qq_to_game_name
from pcr.plugins.get_best_name import get_best_name


@on_command('show_rank', aliases=['排名'], only_to_me=False)
async def show_rank(session: CommandSession):
    if session.event.group_id != config.PRIMARY_GROUP_ID and session.event['message_type'] != 'private':
        print('NOT IN SELECTED GROUP')
        return
    name: str = get_best_name(session)
    name_in_game = qq_to_game_name(name)
    print(name_in_game)
    if name_in_game is None or len(name_in_game) == 0:
        await session.send('没有找到指挥官的排名喵...')
        return
    position_on_today_rank = position_on_rank(calculate_rank(True), name_in_game)
    position_on_overall_rank = position_on_rank(calculate_rank(False), name_in_game)
    message = '指挥官今日排名第%d，总排名第%d，继续加油喵~' % (position_on_today_rank, position_on_overall_rank)
    await session.send(message)


def position_on_rank(rank: list, name: str) -> int:
    current_damage = 9999999999999999
    current_best_index = 1
    for index, element in enumerate(rank):
        # 当多人伤害完全相同的时候，取最高排名
        if element[1] < current_damage:
            current_best_index = index + 1
            current_damage = element[1]
        if element[0] == name:
            return current_best_index
    return -1


def calculate_rank(is_today: bool) -> list:
    """

    :rtype: list format: (player_name, damage)
    """
    c = get_connection()
    if is_today:
        today = int(datetime.now().strftime("%Y%m%d"))
        today_records = c.execute('SELECT username, damage FROM record WHERE date=?', (today,)).fetchall()
        today_rank_list = list_rank(today_records)
        return today_rank_list
    else:
        records = c.execute('SELECT username, damage FROM record').fetchall()
        overall_rank = list_rank(records)
        return overall_rank


def list_rank(records) -> list:
    c = get_connection()
    rank_dict = dict()

    list_of_players = c.execute('SELECT player_name FROM player_list').fetchall()
    for player in list_of_players:
        rank_dict[player[0]] = 0

    for record in records:
        print(record)
        record_name = record[0]
        if record_name in rank_dict:
            rank_dict[record_name] += record[1]

    rank_list: list = list(rank_dict.items())
    rank_list.sort(key=take_damage, reverse=True)  # 根据伤害从高到低排列
    return rank_list


def take_damage(e):
    return e[1]
