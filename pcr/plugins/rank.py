from nonebot import on_command, CommandSession
from data.json.json_editor import JSONEditor
from data.init_database import get_connection
import config
from datetime import datetime
from data.qq_game_name_converter import qq_to_game_name
from pcr.plugins.get_best_name import get_best_name


@on_command('show_rank', aliases=['排名'], only_to_me=False)
async def show_rank(session: CommandSession):
    if session.event.group_id != config.GROUP_ID:
        print('NOT IN SELECTED GROUP')
        return
    name: str = get_best_name(session)
    name_in_game = qq_to_game_name(name)
    if name_in_game is None:
        await session.send('没有找到指挥官的排名喵...')
    position_on_today_rank = calculate_rank(True)


def calculate_rank(is_today: bool) -> list:
    c = get_connection()
    if is_today:
        today = int(datetime.now().strftime("%Y%m%d"))
        today_records = c.execute('SELECT (username, damage) FROM record WHERE date=?', today).fetchall()
        today_rank_list = calculate_rank(today_records)
        return today_rank_list
    else:
        records = c.execute('SELECT (username, damage, date) FROM record').fetchall()
        overall_rank = calculate_rank(records)
        return overall_rank





def calculate_rank(records):
    c = get_connection()
    rank_dict = dict()

    list_of_players = c.execute('SELECT (player_name) FROM player_list').fetchall()
    for player in list_of_players:
        rank_dict[player] = 0

    for record in records:
        record_name = record[0]
        if record_name in rank_dict:
            rank_dict[record_name] += record[1]

    rank_list: list = list(rank_dict.items())
    rank_list.sort(key=take_damage, reverse=True)  # 根据伤害从高到低排列
    return rank_list


def take_damage(e):
    return e[1]
