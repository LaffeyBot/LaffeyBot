from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand
from data.attack_history import get_list_of_attacks
from datetime import datetime, timedelta
import jieba.posseg as psg
import jieba


@on_command('list_attack_detail', aliases=['出刀详情', '出击详情'], only_to_me=False)
async def list_attack_detail(session: CommandSession):
    day = datetime.now()
    day_text = '今天'
    group_id = session.event.group_id
    if session.state.get('yesterday', False):
        day = datetime.now() - timedelta(days=1)
        day_text = '昨天'

    if session.state.get('detail', True):
        record_list: list = get_list_of_attacks(day, group_id)
        custom = session.state.get('custom', '出击')
        message = '下面是' + day_text + '的' + custom.replace('了', '') + '详情喵：\n'
        for item in record_list:
            message += '- ' + item[0] + custom + str(item[1]) + '次\n'
        message += '还请多多' + custom.replace('了', '') + '喵！勤劳才会致富喵！'
        await session.send(message)
    else:
        record_list: list = get_list_of_attacks(day, group_id)
        count_list = count_attack_times(record_list)
        message = '已经有: \n'
        custom = session.state.get('custom', '出击')
        for item in count_list:
            message += '- ' + str(item[1]) + '位指挥官' + custom + item[0] + '次\n'
        message += '还请多多' + custom.replace('了', '') + '喵！勤劳才会致富喵！'
        await session.send(message)


@list_attack_detail.args_parser
async def _(session: CommandSession):
    stripped_arg = session.event.raw_message
    print(stripped_arg)
    if stripped_arg[-2:] not in ['详情', '报告']:
        session.finish()  # 最后两位必须是详情/报告
    if '详情' in stripped_arg:
        session.state['detail'] = True
    else:
        session.state['detail'] = False
    stripped_arg = stripped_arg.replace('详情', '').replace('报告', '')
    if '昨日' in stripped_arg or '昨天' in stripped_arg:
        session.state['yesterday'] = True
        stripped_arg = stripped_arg.replace('昨日', '').replace('昨天', '')
    else:
        session.state['yesterday'] = False

    jieba.load_userdict('user_dict.txt')
    custom = ''
    le_added = False
    for word_pos in psg.cut(stripped_arg):
        custom += word_pos.word
        if not le_added and word_pos.flag == 'v':
            custom += '了'
            le_added = True
    if not le_added:
        custom += '了'
    session.state['custom'] = custom


@on_natural_language(keywords={'详情', '报告'}, only_to_me=False)
async def _(session: NLPSession):
    return IntentCommand(90.0, 'list_attack_detail')


def count_attack_times(record: list) -> list:
    count_dict = dict()
    for element in record:
        if str(element[1]) in count_dict:
            count_dict[str(element[1])] += 1
        else:
            count_dict[str(element[1])] = 1

    count_list: list = list(count_dict.items())
    # [('1', 3)...]
    count_list.sort(key=take_first, reverse=True)
    return count_list


def take_first(e):
    return e[0]
