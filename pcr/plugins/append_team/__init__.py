from nonebot import on_command, CommandSession
from nonebot import get_bot
from data.model import *
from pcr.plugins.capture_team_rank.get_team_rank import *
from nonebot.command.argfilter import extractors
from datetime import datetime
from data.init_database import get_connection
import nonebot


@on_command('add_new_group', aliases=('添加记录公会', '追加记录公会', '记录公会排名'), only_to_me=False)
async def add_new_group(session: CommandSession):
    group_name = session.get('group_name', prompt='请给出添加的公会名称')
    db.init_app(get_bot().server_app)
    s = SpiderTeamRank()
    result = s.get_team_rank_info_by_tname(group_name)
    if result['data']:
        if len(result['data']) > 1:
            message = f'现在有如下多个名叫{group_name}的公会：\n'
            count = 1
            for group in result['data']:
                message += '=========\n'
                message += f'{count}.' + group['clan_name'] + ':\n'
                message += '会长是：' + group['leader_name'] + ' 会长游戏id是：' + str(group['leader_viewer_id'])+' 当前该公会排名为：' +str(group['rank'])+ '\n'
                count += 1
            message += '请使用前面的编号进行选择\n'
            index = session.get(
                'index',
                prompt=message,
                arg_filters=[
                    extractors.extract_text,  # 取纯文本部分
                    str.strip,  # 去掉两边空白字符
                ]
            )
            try:
                index = int(index)
                g = Group()
                r1 = Group.query.filter(Group.name == result['data'][index - 1]['clan_name'],
                                        Group.leader_id == result['data'][index - 1]['leader_viewer_id']).first()
                # FIXME: 对于已经通过QQ创建但是没有 leader_id 的公会，仍然会创建一个不同的新公会以记录排名。
                if not r1:
                    g = Group(
                        name=result['data'][0]['clan_name'],
                        description='这是拉菲bot添加的公会记录喵！',
                        must_request=True,
                        leader_id=result['data'][0]['leader_viewer_id'],
                        is_temp=True
                    )
                    db.session.add(g)
                    db.session.commit()
                    await session.send(f'{g.name}公会添加成功！')
                else:
                    await session.send('该公会记录已经存在了', at_sender=True)
            except ValueError as e:
                await session.send('输入非数字的字符拉菲理解不了QAQ')

        else:
            r2 = Group.query.filter(Group.name == result['data'][0]['clan_name'],
                                    Group.leader_id == result['data'][0]['leader_viewer_id']).first()
            if not r2:
                try:
                    # FIXME: 第38行的查重filter命令在这里也应该被执行
                    g = Group(
                        name=result['data'][0]['clan_name'],
                        description='这是拉菲bot添加的公会记录喵！',
                        must_request= True,
                        leader_id=result['data'][0]['leader_viewer_id'],
                        is_temp= True
                    )
                    db.session.add(g)
                    db.session.commit()
                    await session.send(f'{g.name}公会添加成功！')
                except Exception as e:
                    await session.send('添加失败了喵，请重试', at_sender=True)
                    return
            else:
                await session.send('该公会记录已经存在了', at_sender=True)
    else:
        await session.send(f'{group_name}公会并不存在喵，请重试喵QAQ，若是新改名公会，请半小时后重试', at_sender=True)
        return


@add_new_group.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['group_name'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('格式：【添加记录公会 xxx】')

    session.state[session.current_key] = stripped_arg


@nonebot.scheduler.scheduled_job('cron', minute='*/30')
# @nonebot.scheduler.scheduled_job('cron', second='*/15')
async def get_team_rank_per_half_hour():
    bot = get_bot()
    s = SpiderTeamRank()
    # db.init_app(get_bot().server_app)
    # groups = Group.query.filter(Group.name).all()
    c = get_connection()
    cursor = c.cursor()
    cursor.execute('select * from production.group')
    groups = cursor.fetchall()
    print(groups)
    for g in groups:
        # TODO: 可能需要加几秒的sleep，否则容易被ban。
        print(g)
        result = s.get_team_rank_info_by_tname(g[2])
        g_name = g[2]
        g_leader_id = g[5]
        g_id = g[0]
        print(g_name, g_leader_id)
        if result:
            if not result['data']:
                await bot.send_group_msg(group_id=1108319335,
                                         message=f'{g_name}公会已经查不到排名了，可能是查询网站问题或者是该公会已经改名,请去 https://kengxxiao.github.io/Kyouka/ 查看')
                continue
            for data in result['data']:
                print(1)
                print(g_name, g_leader_id)
                print(data['clan_name'], data['leader_viewer_id'])
                if data['clan_name'] == g_name and data['leader_viewer_id'] == int(g_leader_id):
                    # t1 = TeamRank.query.filter(TeamRank.group_id == g_id).last()
                    cursor.execute(f'select * from team_rank where group_id = {g_id};')
                    print(2)
                    ranks = cursor.fetchall()
                    print(ranks, type(ranks))
                    if ranks:
                        t1 = ranks[-1]
                        if t1 and t1[3] == data['rank']:
                            print('/')
                            continue
                        print('=')
                    # p = Progress()
                    # p.get_result(result['damage'])
                    # TODO: 注意 boss_hp 存储的是boss最大生命值List, 这可能不是你想要的数据。
                    # FIXME: 没有提供 group_id。无法判断这是属于哪一个group的。
                    # epoch = TeamBattleEpoch.query.filter(datetime.now() > TeamBattleEpoch.from_date,
                    #                                      datetime.now() < TeamBattleEpoch.end_date).first()
                    print('?')
                    cursor.execute(
                        f'select * from team_battle_epoch where from_date<DATE(NOW()) and end_date>DATE(NOW());')
                    epoch = cursor.fetchall()
                    print(epoch)
                    print(3)
                    if not epoch:
                        print('非会战期间，不进行更新操作')
                        return

                    # t2 = TeamRank(
                    #     rank=data['rank'],
                    #     total_score=data['damage'],
                    #     record_date=datetime.now(),
                    #     group_id=g_id,
                    #     epoch_id=epoch.id
                    # )
                    #
                    cursor.execute(
                        'insert into team_rank values (%s,%s,%s,%s,%s,%s)',
                        (0, epoch[0][0], g_id, data['rank'], data['damage'], datetime.now())
                    )
                    print(4)
                    c.commit()
                    await bot.send_group_msg(group_id=1108319335,
                                             message=f'{g_name}公会排名更新完毕')
                    # break


@on_command('delete_group_record', aliases=('删除记录公会',), only_to_me=False)
async def delete_group_record(session: CommandSession):
    delete_group = session.get(
        'delete_group',
        prompt='请给出要删除记录排名的公会名称',
        arg_filters=[
            extractors.extract_text,  # 取纯文本部分
            str.strip,  # 去掉两边空白字符
        ]
    )
    groups = Group.query.filter(Group.name == delete_group).all()
    if not groups:
        await session.send('数据库中已经不存在该公会的记录了喵', at_sender=True)
        return
    if len(groups) > 1:
        count = 1
        message = f'以下是数据库中所有关于{delete_group}公会信息：\n'
        for group in groups:
            message += '=========\n'
            message += f'{count}' + '. ' + group.name + ':\n'
            message += '会长游戏id是：' + group.leader_id + '\n'
            count += 1
        message += '请使用前面的编号进行选择\n'
        index = session.get(
            'index',
            prompt=message,
            arg_filters=[
                extractors.extract_text,  # 取纯文本部分
                str.strip,  # 去掉两边空白字符
            ]
        )
        try:
            index = int(index)
            g = groups[index - 1]
            delete_item(g)

        except ValueError as e:
            await session.send('输入非数字的字符拉菲理解不了QAQ')
    else:
        delete_item(groups[0])


def delete_item(group: Group):
    db.session.delete(group)
    db.session.commit()


@delete_group_record.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['delete_group'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('格式：【删除记录公会 xxx】')

    session.state[session.current_key] = stripped_arg
