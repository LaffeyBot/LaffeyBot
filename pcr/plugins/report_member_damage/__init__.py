from nonebot import on_command, CommandSession
from data.init_database import get_connection
from datetime import datetime
from .bar_chart import MemberDamageChart
import os
import config
import time as t


@on_command('report_member_daily_damage', aliases=("每日伤害", '成员每日伤害统计'), only_to_me=False)
async def report_member_daily_damage(session: CommandSession):
    group_id = session.event.group_id
    month = '%02d'%datetime.now().month
    day = '%02d'%datetime.now().day
    date = f'{datetime.now().year}{month}{day}'
    print(group_id,date)
    print( 'select username,sum(damage) as sdamage from record where group_id=%s and date=%s group by username;'
            %(group_id, date))
    if group_id:
        cursor = get_connection().cursor()
        cursor.execute(
            'select username,sum(damage) as sdamage from record where group_id=%s and date=%s group by username;',
            (group_id, date))
        result = cursor.fetchall()
        player_name = []
        sdamage = []
        if result:
            for row in result:
                player_name.append(row[0])
                sdamage.append(int(row[1]))
        else:
            await session.send('暂时还没有成员伤害数据喵~')
        file_name = f'{date}_{group_id}_member_damage_statistic.jpg'
        file_path = os.path.join(config.CQ_SOURCE_PATH, 'image', file_name)
        m = MemberDamageChart(title_name=f'{date}公会成员伤害统计', player_name=player_name, damage=sdamage,
                              file_path=file_path)
        m.get_chart()
        percent = round(max(sdamage) / sum(sdamage),4) * 100
        max_player_name = m.sort_damage()[max(sdamage)]
        message = f'以下是今日各位指挥官伤害统计喵~\n' \
                  f'其中伤害最高的指挥官{max_player_name}贡献了今日全队的{percent}%输出喵~\n' \
                  f'[CQ:image,file={file_name}]'
        await session.send(message)


@on_command('report_member_total_damage', aliases=("伤害统计", '成员伤害统计'), only_to_me=False)
async def report_member_total_damage(session: CommandSession):
    group_id = session.event.group_id
    month = '%02d' % datetime.now().month
    day = '%02d' % datetime.now().day
    date = f'{datetime.now().year}{month}'
    if group_id:
        cursor = get_connection().cursor()
        cursor.execute('select username,sum(damage) as sdamage from record where group_id=%s group by username;',
                       (group_id,))
        result = cursor.fetchall()
        player_name = []
        sdamage = []
        if result:
            for row in result:
                player_name.append(row[0])
                sdamage.append(int(row[1]))
        else:
            await session.send('暂时还没有成员伤害数据喵~')
        file_name = f'{date}_{group_id}_member_total_damage_statistic.jpg'
        file_path = os.path.join(config.CQ_SOURCE_PATH, 'image', file_name)
        m = MemberDamageChart(title_name=f'{date}月公会战成员总伤害统计', player_name=player_name, damage=sdamage,
                              file_path=file_path)
        m.get_chart()
        percent = round(max(sdamage) / sum(sdamage),4) * 100
        max_player_name = m.sort_damage()[max(sdamage)]

        message = f'以下是各位指挥官总伤害统计喵~\n' \
                  f'其中伤害最高的指挥官{max_player_name}贡献了全队的{percent}%输出喵~\n' \
                  f'[CQ:image,file={file_name}]'
        await session.send(message)
