import config
from nonebot import on_command, CommandSession
from .calculate_mines import get_mines


@on_command('calculate_mine_jjc', aliases=('挖矿', '竞技场挖矿'), only_to_me=False)
async def calculate_mine_jjc(session: CommandSession):
    ranks = session.get('ranks', prompt='请指挥官给出当前赛季最高排名，历史最高排名，目标排名（不给这项默认登顶）喵~')
    rank_ls = ranks.split(' ')
    print(rank_ls)
    if len(rank_ls) == 2:
        await session.send(get_mines(rank_ls[0], rank_ls[1]))
    elif len(rank_ls) == 3:
        await session.send(get_mines(rank_ls[0], rank_ls[1], rank_ls[2]))
    else:
        await session.send('喵！指挥官需要按要求给出排名才能计算的说喵！')
