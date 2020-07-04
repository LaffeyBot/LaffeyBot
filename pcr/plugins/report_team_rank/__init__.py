from nonebot import on_command,CommandSession
from data.init_database import get_connection
from aiocqhttp import MessageSegment
from .team_rank_quota import TeamRankChart
import config
import os


on_command('query_team_rank', aliases=('实时排名','公会排名','公会战排名'), only_to_me=False)
async def query_team_rank(session:CommandSession):
    if session.event.group_id == config.GROUP_ID:
        result = get_connection().execute('select * from rank_record').fetchall()
        if result:
            times = [t[0] for t in result]
            ranks = [r[1] for r in result]
        file_path = os.path.join(config.TEAM_RANK_CHART_PATH,f'{times[-1]}_team_rank.jpg')
        tc = TeamRankChart(times,ranks,file_path)
        tc.get_chart()
        seq = MessageSegment(type_='image', data={'file': file_path})
        message = f'当前公会排名是：{ranks[-1]}(拉菲这里是每小时一更新，数据可能会有偏差)\n'
        if len(times)<=2:
            await session.send(message)
        else:
            await session.send(message+seq)
        if os.path.exists(file_path):
            os.remove(file_path)







