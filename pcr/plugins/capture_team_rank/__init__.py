from nonebot import on_command, CommandSession
from .get_team_rank import SpiderTeamRank
import time


@on_command('query_team_rank_by_tname', aliases=('公会排名查询',), only_to_me=False)
async def query_team_rank_by_tname(session: CommandSession):
    tname = session.get('tname', prompt='请指挥官给出要查询的公会名称喵~')
    # message = ''
    s = SpiderTeamRank()
    result = s.get_team_rank_info_by_tname(tname)
    if result:
        message = '已经为指挥官查到如下结果：\n'
    else:
        message = f'没有查询到{tname}公会的消息喵QAQ~'
        await session.send(message, at_sender=True)
        return
    data = result['data']
    if not data:
        message = f'没有查询到{tname}公会的消息喵QAQ~'
        await session.send(message, at_sender=True)
        return
    count = 0
    for item in data:
        message += '\n==========\n'
        print(item)
        count += 1
        message += count + '.' + item['clan_name'] + ':\n' + '会长是:' + item['leader_name'] + ',' + '当前排名:' + str(
            item['rank']) + ',会员数:' + \
                   str(item['member_num'])
    await session.send(message, at_sender=True)


@query_team_rank_by_tname.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['tname'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('格式：【公会排名查询 xxx】')

    session.state[session.current_key] = stripped_arg


@on_command('query_team_rank_by_rank', aliases=('排名查公会',), only_to_me=False)
async def query_team_rank_by_rank(session: CommandSession):
    rank = session.get('rank', prompt='请指挥官给出要查询的排名喵~')
    # message = ''
    s = SpiderTeamRank()
    try:
        rank = int(rank)
    except Exception as e:
        await session.send('指挥官好像输入了奇怪的东西nya~', at_sender=True)
    result = s.get_team_rank_info_by_rank(rank)
    if result:
        message = '已经为指挥官查到如下结果：\n'
    else:
        message = f'没有查询到排名为{rank}公会的消息喵QAQ~'
        await session.send(message, at_sender=True)
        return
    data = result['data']
    if not data:
        message = f'没有查询到排名为{rank}公会的消息喵QAQ~'
        await session.send(message, at_sender=True)
        return
    count = 0
    for item in data:
        message += '\n==========\n'
        print(item)
        count += 1
        message += count + '.' + item['clan_name'] + ':\n' + '会长是:' + item['leader_name'] + ',' + '当前排名:' + str(
            item['rank']) + ',会员数:' + \
                   str(item['member_num'])

    await session.send(message, at_sender=True)


@query_team_rank_by_rank.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['rank'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('格式：【排名查公会 xxx】')

    session.state[session.current_key] = stripped_arg
