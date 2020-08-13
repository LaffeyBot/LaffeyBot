from nonebot import on_command, CommandSession
from data.init_database import get_connection
from datetime import datetime
from .bar_chart import MemberDamageChart
from nonebot.command.argfilter import extractors, validators
import os
import config
import time as t


@on_command('report_member_daily_damage', aliases=("每日伤害", '成员每日伤害统计'), only_to_me=False)
async def report_member_daily_damage(session: CommandSession):
    group_id = session.event.group_id
    month = '%02d' % datetime.now().month
    day = '%02d' % datetime.now().day
    date = f'{datetime.now().year}{month}{day}'
    print(group_id, date)
    print('select username,sum(damage) as sdamage from record where group_id=%s and date=%s group by username;'
          % (group_id, date))
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
        percent = round(max(sdamage) / sum(sdamage), 4) * 100
        max_player_name = m.sort_damage()[max(sdamage)]
        message = f'以下是今日各位指挥官伤害统计喵~\n' \
                  f'其中伤害最高的指挥官{max_player_name}贡献了今日全队的{percent}%输出喵~\n' \
                  f'[CQ:image,file={file_name}]'
        await session.send(message)
        if os.path.exists(file_path):
            os.remove(file_path)


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
        file_path = os.path.join(config.CQ_SOURCE_PATH, 'images', file_name)
        m = MemberDamageChart(title_name=f'{date}月公会战成员总伤害统计', player_name=player_name, damage=sdamage,
                              file_path=file_path)
        m.get_chart()
        percent = round(max(sdamage) / sum(sdamage), 4) * 100
        max_player_name = m.sort_damage()[max(sdamage)]

        message = f'以下是各位指挥官总伤害统计喵~\n' \
                  f'其中伤害最高的指挥官{max_player_name}贡献了全队的{percent}%输出喵~\n' \
                  f'[CQ:image,file={file_name}]'
        await session.send(message)
        if os.path.exists(file_path):
            os.remove(file_path)


@on_command('damage_report', aliases=('伤害报告',), only_to_me=False)
async def damage_report(session: CommandSession):
    group_id = session.event.group_id
    month = '%02d' % datetime.now().month
    day = '%02d' % datetime.now().day
    date = f'{datetime.now().year}{month}{day}'
    '''if 'pname' not in session.state:
        await session.send('请给出要查询的报告的指挥官名字喵~')
        session.get('pname', arg_filters=[extractors.extract_text])
    player_name = session.state['pname']'''
    info = session.get('info', prompt='请给出要查询的报告的指挥官名字喵~')
    info_ls = info.split()
    if len(info_ls) == 1:
        player_name = info_ls[0]
    elif len(info_ls) == 2:
        player_name = info_ls[0]
        date = info_ls[1]
    else:
        await session.send('喵！指挥官需要按要求给出才能计算的说喵！')
    print(player_name, date)
    if group_id:
        if date != '*':
            cursor = get_connection().cursor()
            cursor.execute('select username,target,damage from record where group_id=%s and date=%s and username=%s;',
                           (group_id, date, player_name))
            result = cursor.fetchall()
            message = f'以下是{player_name}指挥官{date}出刀报告：\n'
            if result:
                for row in result:
                    message += f'- 出刀{row[1]} 造成了{row[2]}点伤害\n'
                await session.send(message)
            else:
                await session.send('没有查询到相关指挥官的出刀信息喵QAQ')
        else:
            cursor = get_connection().cursor()
            cursor.execute('select username,target,damage,date from record where group_id=%s and username=%s;',
                           (group_id, player_name))
            result = cursor.fetchall()
            message = f'以下是{player_name}指挥官会战期间出刀报告：\n'
            target = []
            damage = []
            if result:
                for row in result:
                    message += f'{row[3]}日 出刀{row[1]} 造成了{row[2]}点伤害\n'
                    target.append(f'{row[3]}的{row[1]}')
                    damage.append(row[2])
                message += f'该指挥官会战期间累计造成了{sum(damage)}点伤害喵~'
                await session.send(message)
            else:
                await session.send('暂时还没有成员伤害数据喵~')
            file_name = f'{group_id}_{player_name}_member_damage_statistic.jpg'
            file_path = os.path.join(config.CQ_SOURCE_PATH, 'images', file_name)
            m = MemberDamageChart(title_name=f'{player_name}公会战伤害统计', player_name=target, damage=damage,
                                  file_path=file_path)
            print(file_path)
            m.get_chart()
            await session.send(f'[CQ:image,file={file_name}]')
            if os.path.exists(file_path):
                os.remove(file_path)
