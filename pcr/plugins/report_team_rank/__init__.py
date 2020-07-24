from nonebot import on_command, CommandSession
from data.init_database import get_connection
from aiocqhttp import MessageSegment
from .team_rank_quota import TeamRankChart
import config
import os


@on_command('query_team_rank', aliases=('实时排名', '公会排名', '公会战排名'), only_to_me=False)
async def query_team_rank(session: CommandSession):
    cursor = get_connection().cursor()
    group_id: int = session.event.group_id
    cursor.execute('select * from rank_record WHERE group_id=%s', (group_id, ))
    result = cursor.fetchall()
    times = []
    ranks = []
    if result:
        """times = [t[0] for t in result]
        ranks = [r[1] for r in result]"""
        for row in result:
            if len(ranks) > 0 and (row[1]>sum(ranks)//len(ranks)+20000 or row[1]<sum(ranks)//len(ranks)-5000):
                continue
            times.append(row[0])
            ranks.append(row[1])
    else:
        await session.send('暂时还没有公会排名记录的喵！>_<')
        return

    file_name = f'{times[-1]}_team_rank_{str(group_id)}.jpg'
    file_path = os.path.join(config.TEAM_RANK_CHART_PATH, file_name)
    tc = TeamRankChart(times, ranks, file_path)
    tc.get_chart()
    print(file_path)
    seq = MessageSegment(type_='image', data={'file': file_name})
    print(ranks)
    message = f'当前公会排名是：{ranks[-1]}'
    if len(times) <= 2:
        await session.send(message)
    else:
        await session.send(message)
        # print('1')
        await session.send(seq)
    if os.path.exists(file_path):
        os.remove(file_path)
