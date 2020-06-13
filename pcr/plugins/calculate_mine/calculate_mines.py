import config


async def get_mines(current_rank, history_rank, aim_rank='1'):
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
    if crank > 16000 or hrank > 16000 or arank > 16000:
        message += '喵？一个场的jjc/pjjc可没那么多的指挥官喵...nya'
        return message
    if crank < 1 or hrank < 1 or arank < 1:
        message += '喵？指挥官又在异想天开了喵！排名不可能是小于1的喵！'
        return message
    if crank < arank:
        crank, arank = arank, crank
        message += f'指挥官当前赛季最高排名{crank}和目标排名{arank}写反了喵，{config.MY_NAME}已经修复了喵~\n'
    if crank < hrank:
        message += f'喵？指挥官怎么的当前赛季最高排名{crank}怎么会比历史排名{hrank}高？\n' \
                   f'指挥官怎么了？…难道是坏掉了？需要我修修喵？'
        return message
    mine = await calculate(crank,arank,hrank)
    message += f'喵，根据计算，指挥官还能获得{mine}的钻石~继续加油吧！'
    return message


season_sequence_list = [i for i in config.SEASON_SEQUENT_DIC]
season_discrete_list = [i for i in config.SEASON_DISCRETE_DIC]
history_sequence_list = [i for i in config.HISTORY_SEQUENT_DIC]
history_discrete_list = [i for i in config.HISTORY_DISCRETE_DIC]


async def calculate(crank, arank, hrank):
    mines = 0
    if arank <= hrank:
        # 超不过历史最佳
        ci, cst = get_range(crank, season_sequence_list, season_discrete_list)
        ai, ast = get_range(arank, season_sequence_list, season_discrete_list)
        if cst == 0 and ast == 0:
            if ci == ai:
                mines += config.SEASON_SEQUENT_DIC[season_sequence_list[ci]] * (hrank - arank)
            else:
                for i in range(ai, ci):
                    mines += config.SEASON_SEQUENT_DIC[season_sequence_list[i]] * (
                            season_sequence_list[i + 1] - season_sequence_list[i])
                mines += config.SEASON_SEQUENT_DIC[season_sequence_list[ci]] * (crank - season_sequence_list[ci])
                mines -= config.SEASON_SEQUENT_DIC[season_sequence_list[ai]] * (arank - season_sequence_list[ai])
        elif cst == 1 and ast == 0:
            for i in range(ai, len(season_sequence_list)):
                if i != len(season_sequence_list) - 1:
                    mines += config.SEASON_SEQUENT_DIC[season_sequence_list[i]] * (
                            season_sequence_list[i + 1] - season_sequence_list[i])
                else:
                    mines += config.SEASON_SEQUENT_DIC[season_sequence_list[i]] * (
                            season_discrete_list[0] - season_sequence_list[i])
            mines -= config.SEASON_SEQUENT_DIC[season_sequence_list[ai]] * (arank - season_sequence_list[ai])
            for j in range(ci + 1):
                mines += config.SEASON_DISCRETE_DIC[season_discrete_list[j]] * (
                        season_discrete_list[j + 1] // 100 - season_discrete_list[j] // 100)
            mines -= config.SEASON_DISCRETE_DIC[season_discrete_list[ci]] * (
                    season_discrete_list[ci + 1] // 100 - crank // 100)
        elif cst == 1 and ast == 1:
            if ci == ai:
                mines += config.SEASON_DISCRETE_DIC[season_discrete_list[ci]] * (crank // 100 - arank // 100)
            else:
                for i in range(ai, ci):
                    mines += config.SEASON_DISCRETE_DIC[season_discrete_list[i]] * (
                            season_discrete_list[i + 1] // 100 - season_discrete_list[i] // 100)
                mines += config.SEASON_DISCRETE_DIC[season_discrete_list[ci]] * (
                        crank // 100 - season_discrete_list[ci] // 100)
                mines -= config.SEASON_DISCRETE_DIC[season_discrete_list[ai]] * (
                        arank // 100 - season_discrete_list[ai] // 100)
        return mines
    else:
        ci, cst = get_range(crank, season_sequence_list, season_discrete_list)
        ai, ast = get_range(arank, season_sequence_list, season_discrete_list)
        if cst == 0 and ast == 0:
            if ci == ai:
                mines += config.SEASON_SEQUENT_DIC[season_sequence_list[ci]] * (crank - arank)
            else:
                for i in range(ai, ci):
                    mines += config.SEASON_SEQUENT_DIC[season_sequence_list[i]] * (
                            season_sequence_list[i + 1] - season_sequence_list[i])
                mines += config.SEASON_SEQUENT_DIC[season_sequence_list[ci]] * (crank - season_sequence_list[ci])
                mines -= config.SEASON_SEQUENT_DIC[season_sequence_list[ai]] * (arank - season_sequence_list[ai])
        elif cst == 1 and ast == 0:
            for i in range(ai, len(season_sequence_list)):
                if i != len(season_sequence_list) - 1:
                    mines += config.SEASON_SEQUENT_DIC[season_sequence_list[i]] * (
                            season_sequence_list[i + 1] - season_sequence_list[i])
                else:
                    mines += config.SEASON_SEQUENT_DIC[season_sequence_list[i]] * (
                            season_discrete_list[0] - season_sequence_list[i])
            mines -= config.SEASON_SEQUENT_DIC[season_sequence_list[ai]] * (arank - season_sequence_list[ai])
            for j in range(ci + 1):
                mines += config.SEASON_DISCRETE_DIC[season_discrete_list[j]] * (
                        season_discrete_list[j + 1] // 100 - season_discrete_list[j] // 100)
            mines -= config.SEASON_DISCRETE_DIC[season_discrete_list[ci]] * (
                    season_discrete_list[ci + 1] // 100 - crank // 100)
        elif cst == 1 and ast == 1:
            if ci == ai:
                mines += config.SEASON_DISCRETE_DIC[season_discrete_list[ci]] * (crank // 100 - arank // 100)
            else:
                for i in range(ai, ci):
                    mines += config.SEASON_DISCRETE_DIC[season_discrete_list[i]] * (
                            season_discrete_list[i + 1] // 100 - season_discrete_list[i] // 100)
                mines += config.SEASON_DISCRETE_DIC[season_discrete_list[ci]] * (
                        crank // 100 - season_discrete_list[ci] // 100)
                mines -= config.SEASON_DISCRETE_DIC[season_discrete_list[ai]] * (
                        arank // 100 - season_discrete_list[ai] // 100)
        if arank > hrank:
            hi, hst = get_range(hrank, history_sequence_list, history_discrete_list)
            if ast == 0 and hst == 0:
                if hi == ai:
                    mines += config.HISTORY_SEQUENT_DIC[history_sequence_list] * (hrank - arank)
                else:
                    for i in range(ai, hi):
                        mines += config.HISTORY_SEQUENT_DIC[history_sequence_list[i]] * (
                                history_sequence_list[i + 1] - history_sequence_list[i])
                    mines += config.HISTORY_SEQUENT_DIC[history_sequence_list[ci]] * (hrank - history_sequence_list[hi])
                    mines -= config.HISTORY_SEQUENT_DIC[history_sequence_list[ai]] * (arank - history_sequence_list[ai])
            elif ast == 0 and hst == 1:
                for i in range(ai, len(history_sequence_list)):
                    if i != len(history_sequence_list) - 1:
                        mines += config.HISTORY_SEQUENT_DIC[history_sequence_list[i]] * (
                                history_sequence_list[i + 1] - history_sequence_list[i])
                    else:
                        mines += config.HISTORY_SEQUENT_DIC[history_sequence_list[i]] * (
                                history_discrete_list[0] - history_sequence_list[i])
                mines -= config.HISTORY_SEQUENT_DIC[history_sequence_list[ai]] * (arank - history_sequence_list[ai])
                for j in range(ci + 1):
                    mines += config.HISTORY_DISCRETE_DIC[history_discrete_list[j]] * (
                            history_discrete_list[j + 1] // 100 - history_discrete_list[j] // 100)
                mines -= config.HISTORY_DISCRETE_DIC[history_discrete_list[hi]] * (
                        history_discrete_list[hi + 1] // 100 - hrank // 100)
            elif ast == 1 and hst == 1:
                if hi == ai:
                    mines += config.HISTORY_DISCRETE_DIC[history_discrete_list[hi]] * (hrank // 100 - arank // 100)
                else:
                    for i in range(ai, ci):
                        mines += config.HISTORY_DISCRETE_DIC[history_discrete_list[i]] * (
                                history_discrete_list[i + 1] // 100 - history_discrete_list[i] // 100)
                    mines += config.HISTORY_DISCRETE_DIC[history_discrete_list[hi]] * (
                            hrank // 100 - history_discrete_list[hi] // 100)
                    mines -= config.HISTORY_DISCRETE_DIC[history_discrete_list[ai]] * (
                            arank // 100 - history_discrete_list[ai] // 100)
        return mines


async def get_range(rank, sl, dl):
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
