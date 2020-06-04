from nonebot import on_command, CommandSession, permission as perm
from data.damage import delete_all_records, add_record
from data.attack_history import get_list_of_attacks
from datetime import datetime, timedelta


@on_command('list_attacks', aliases=['出刀报告', '出击报告'], only_to_me=False)
async def list_attacks(session: CommandSession):
    record_list: list = get_list_of_attacks(datetime.now())
    count_list = count_attack_times(record_list)
    message = '已经有: \n'
    for item in count_list:
        message += '- ' + str(item[1]) + '位指挥官出击了' + item[0] + '次\n'
    message += '还请多多出击喵！勤劳才会致富喵！'
    await session.send(message)


@on_command('list_attack_detail', aliases=['出刀详情', '出击详情'], only_to_me=False)
async def list_attack_detail(session: CommandSession):
    record_list: list = get_list_of_attacks(datetime.now())
    message = '下面是今天的出击详情喵：\n'
    for item in record_list:
        message += '- ' + item[0] + '出击了' + str(item[1]) + '次\n'
    message += '还请多多出击喵！勤劳才会致富喵！'
    await session.send(message)


@on_command('list_attacks_yesterday', aliases=['昨日出刀报告', '昨日出击报告', '昨天出刀'], only_to_me=False)
async def list_attacks(session: CommandSession):
    record_list: list = get_list_of_attacks(datetime.now() - timedelta(days=1))
    count_list = count_attack_times(record_list)
    message = '昨日出击报告： \n'
    for item in count_list:
        message += '- ' + str(item[1]) + '位指挥官出击了' + item[0] + '次\n'
    message += '还请多多出击喵！勤劳才会致富喵！'
    await session.send(message)


@on_command('list_attack_detail', aliases=['昨日出刀详情', '昨日出击详情'], only_to_me=False)
async def list_attack_detail(session: CommandSession):
    record_list: list = get_list_of_attacks(datetime.now() - timedelta(days=1))
    message = '下面是昨天的出击详情喵：\n'
    for item in record_list:
        message += '- ' + item[0] + '出击了' + str(item[1]) + '次\n'
    message += '还请多多出击喵！勤劳才会致富喵！'
    await session.send(message)


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
