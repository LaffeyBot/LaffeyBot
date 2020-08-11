from nonebot import on_command, CommandSession
from data.init_database import get_connection
from aiocqhttp import MessageSegment
from .team_rank_quota import TeamRankChart
from datetime import datetime
import config
import os


@on_command('query_team_rank', aliases=('实时排名', '公会排名', '公会战排名'), only_to_me=False)
async def query_team_rank(session: CommandSession):
    cursor = get_connection().cursor()
    group_id: int = session.event.group_id
    cursor.execute('select * from rank_record WHERE group_id=%s', (group_id,))
    result = cursor.fetchall()
    times = []
    ranks = []
    if result:
        """times = [t[0] for t in result]
        ranks = [r[1] for r in result]"""
        for row in result:
            if len(ranks) > 0 and (
                    row[2] > sum(ranks) // len(ranks) + 20000 or row[2] < sum(ranks) // len(ranks) - 5000):
                continue
            times.append(row[1])
            ranks.append(row[2])
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


@on_command('report_rank', aliases=('上报排名', '更新公会排名'))
async def report_rank(session: CommandSession):
    group_id = session.event.group_id
    month = '%02d' % datetime.now().month
    day = '%02d' % datetime.now().day
    date = f'{datetime.now().year}{month}{day}'
    # 判断是否在公会群
    c = get_connection()
    cursor = c.cursor()
    cursor.execute('select * from group_list WHERE group_id=%s', (group_id,))
    group_result = cursor.fetchall()
    if group_result:
        # 判断是否有这个记录了
        cursor.execute('select * from rank_record WHERE group_id=%s and date=%s', (group_id, date))
        rank_result = cursor.fetchone()
        if rank_result:
            await session.send(f'当前已经存在公会排名数据为{rank_result[2]}')
        else:
            rank = await session.get('rank', prompt='请指挥官给出当前公会排名喵~')
            try:
                cursor.execute('insert into rank_record (date,rank,group_id) values (%s,%s,%s)', (date, rank, group_id))
                c.commit()
            except Exception as e:
                print(e)
                await session.send('数据提交失败了喵~请重试喵~')
                c.rollback()

    else:
        await session.send('该群还不是公会群，请先设置为公会群再执行本命令喵~')


@on_command('modify_rank', aliases=('修改排名', '更改公会排名'))
async def report_rank(session: CommandSession):
    group_id = session.event.group_id
    # month = '%02d' % datetime.now().month
    # day = '%02d' % datetime.now().day
    # date = f'{datetime.now().year}{month}{day}'
    # 判断是否在公会群
    c = get_connection()
    cursor = c.cursor()
    cursor.execute('select * from group_list WHERE group_id=%s', (group_id,))
    group_result = cursor.fetchall()
    if group_result:
        # 判断是否有这个记录了
        cursor.execute('select * from rank_record WHERE group_id=%s and date=%s', (group_id, date))
        rank_result = cursor.fetchone()
        if rank_result:
            await session.send(f'当前已经存在公会排名数据为{rank_result[2]}')
            while True:
                current_info = session.get('current_info', prompt='请指挥官给出日期(格式为20200701这种)和当前公会排名')
                info = current_info.split()
                if int(info[1]) != rank_result[2]:
                    break
                else:
                    await session.send('不能和当前排名一样喵~')
            try:
                cursor.execute(
                    f'update rank_record set date={int(info[0])},rank={int(info[1])} where group_id = {group_id}')
                c.commit()
            except Exception as e:
                print(e)
                c.rollback()
                await session.send('排名更新失败了喵，请重试喵')
        else:
            await session.send('没有找到相关可以修改的记录喵QAQ')

    else:
        await session.send('该群还不是公会群，请先设置为公会群再执行本命令喵~')
