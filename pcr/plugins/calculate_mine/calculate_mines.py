import config
from .mine_quota import Season_nonsequence_mine, Season_sequence_mine, History_nonsequence_mine, History_sequence_mine


def get_mines(current_rank, history_rank, aim_rank='1'):
    '''crank = 15001
    arank = 15001
    hrank = 15001'''
    message = ''
    try:
        crank = int(current_rank)
        arank = int(aim_rank)
        hrank = int(history_rank)
        print(crank)
    except ValueError as e:
        message += f'当前赛季最高排名{current_rank}/目标排名{aim_rank}/历史最高排名{history_rank}要都是数字才行的喵~'
        return message
    if crank > 15050 or hrank > 15050 or arank > 15050:
        message += '喵？一个场的jjc/pjjc可没那么多的指挥官喵...nya'
        return message
    if crank < 1 or hrank < 1 or arank < 1:
        message += '喵？指挥官又在白日做梦了喵！排名不可能是小于1的喵！'
        return message
    if crank < arank:
        crank, arank = arank, crank
        message += f'指挥官当前赛季最高排名{crank}和目标排名{arank}写反了喵，{config.MY_NAME}已经修复了喵~\n'
    if crank < hrank:
        message += f'喵？指挥官怎么的当前赛季最高排名{crank}怎么会比历史排名{hrank}高？\n' \
                   f'指挥官怎么了？…难道是坏掉了？需要我修修喵？'
        return message
    mine = calculate(crank, arank, hrank)
    message += f'喵，根据计算，指挥官还能获得{mine}的钻石~继续加油吧！'
    return message


season_sequence_list = [i for i in config.SEASON_SEQUENT_DIC]
season_discrete_list = [i for i in config.SEASON_DISCRETE_DIC]
history_sequence_list = [i for i in config.HISTORY_SEQUENT_DIC]
history_discrete_list = [i for i in config.HISTORY_DISCRETE_DIC]
sl = []
hl = []


def init(ssl, sdl, hsl, hdl):
    for i in range(len(ssl)):
        if i == len(ssl) - 1:
            s = Season_sequence_mine(ssl[i], sdl[0], config.SEASON_SEQUENT_DIC[ssl[i]])
        else:
            s = Season_sequence_mine(ssl[i], ssl[i + 1], config.SEASON_SEQUENT_DIC[ssl[i]])
        sl.append(s)
    for i in range(len(sdl)):
        if i == len(sdl) - 1:
            s = Season_nonsequence_mine(sdl[i], 15050, config.SEASON_DISCRETE_DIC[sdl[i]])
        else:
            s = Season_nonsequence_mine(sdl[i], sdl[i + 1], config.SEASON_DISCRETE_DIC[sdl[i]])
        sl.append(s)
    for i in range(len(hsl)):
        if i == len(hsl) - 1:
            h = History_sequence_mine(hsl[i], hdl[0], config.HISTORY_SEQUENT_DIC[hsl[i]])
        else:
            h = History_sequence_mine(hsl[i], hsl[i + 1], config.HISTORY_SEQUENT_DIC[hsl[i]])
        hl.append(h)
    for i in range(len(hdl)):
        if i == len(hdl) - 1:
            h = History_nonsequence_mine(hdl[i], 15050, config.HISTORY_DISCRETE_DIC[hdl[i]])
        else:
            h = History_nonsequence_mine(hdl[i], hdl[i + 1], config.HISTORY_DISCRETE_DIC[hdl[i]])
        hl.append(h)


def calculate(crank, arank, hrank):
    init(season_sequence_list, season_discrete_list, history_sequence_list, history_discrete_list)
    for i in sl:
        print(i.start_rank,i.per_mine,i.end_rank)
    print('===')
    for j in hl:
        print(j.start_rank,j.per_mine,j.end_rank)
    print("====")
    print(f'当前排名{crank}目标排名{arank},历史最高排名{hrank}')
    if arank >= hrank:
        mines = count(arank, crank, sl)
    else:
        mines = count(arank, crank, sl) + count(arank, crank, hl)
    print(sl)
    print(hl)
    return mines


def count(sr, er, ls):
    for i in range(len(ls)):
        if ls[i].is_this_range(sr):
            break
    for j in range(len(ls)):
        if ls[j].is_this_range(er):
            break
    print(i,j)
    if i == j:
        return ls[i].range_in_mine(sr, er)
    else:
        result = ls[i].get_after_mine(sr) + ls[j].get_before_mine(er)
        for k in range(i + 1, j):
            result += ls[k].range_mine_calculate()
        return result


def get_range(rank, sl, dl):
    # 确定每个排名都处在什么奖励范围上的
    if rank < dl[0]:
        # 在第一梯队
        for i in range(len(sl)):
            if sl[i] <= rank and sl[i + 1] > rank:
                return i, 0
    else:
        # 在第二梯队
        for i in range(len(dl)):
            if dl[i] <= rank and dl[i + 1] > rank:
                return i, 1




