from nonebot import on_command, CommandSession
from .get_calender import calender_info
from datetime import datetime
from dateutil.parser import parse
import datetime
import nonebot
import re
import asyncio


@on_command('calender', aliases=('日程表', '日历', '未来活动'), only_to_me=False)
async def calender(session: CommandSession):
    plan_info = calender_info()
    if isinstance(plan_info[0], str):
        await session.send(plan_info[0], at_sender=True)
        return

    message = ''
    future_date = [datetime.datetime.today() + datetime.timedelta(i) for i in range(5)]
    for check_date in future_date:
        events = []
        for target in plan_info:
            start_time = target['start_time']
            end_time = target['end_time']
            if parse(start_time) <= check_date <= parse(end_time):
                events.append(target['name'])
        message += f'===={check_date.strftime("%Y{y}%m{m}%d{d}").format(y="年", m="月", d="日")}====\n'
        if len(events) > 0:
            for event in events:
                message += f'>>{event}\n'
        else:
            message += '今日还暂时没有活动喵QAQ\n'

    message += '更多日程请查看：https://tools.yobot.win/calender/#cn'
    await session.send(message)


def get_tips()->list:
    future_date = [
        (datetime.datetime.today() + datetime.timedelta(i)).strftime("%Y{y}%m{m}%d{d}").format(y="年", m="月", d="日") for i in
        range(3)]
    tips = [
        f"1、{future_date[0]} 18点前领取最后一次家具体力，{future_date[0]} 18点-{future_date[1]}18点 之间不再领取家具体力\n"
        f"2、{future_date[1]} 每日200体力 等18点以后领取\n"
        f"3、{future_date[1]} 18点以后，自回体保证在71~79+每日200体力+额外买6管体力，使体力≥991\n"
        f"4、{future_date[1]} 完成第三步后，点赞（10点体力），领取家具体力，都会存入邮箱保持24小时，然后下线\n"
        f"5、{future_date[2]} 起床开刷N2",
        f"{future_date[1]}开始困难碎片获取翻倍，请各位指挥官提前准备好本期要刷的目标角色碎片",
        f"{future_date[0]} 留地下城boss不打\n"
        f"{future_date[1]} 把留下的地下城boss打了，然后进入今天地下城不打\n"
        f"{future_date[2]} 记得今天地下城可以打两次喵~",
    ]
    return tips


@nonebot.scheduler.scheduled_job('cron', hour="6-23/6", minute="20")
async def send_tips():
    bot = nonebot.get_bot()
    plan_info = calender_info()
    if isinstance(plan_info[0], str):
        # 没有获取到数据，请求被拒绝了
        return
    tomorrow_start = []  # 明天开启事件
    day_after_tomorrow_start = []  # 后天开启事件
    event_end = []  # 明天结束事件
    future_date = [(datetime.datetime.today() + datetime.timedelta(i)).strftime("%Y-%m-%d") for i in range(3)]
    for event in plan_info:
        # 要将日期换成天的形式，否则时间判断会出问题
        start_time = datetime.datetime.strptime(event['start_time'],"%Y/%m/%d %H:%M:%S").strftime("%Y-%m-%d")
        end_time = datetime.datetime.strptime(event['end_time'],"%Y/%m/%d %H:%M:%S").strftime("%Y-%m-%d")
        in_today = parse(start_time) <= parse(future_date[0]) <= parse(end_time)
        in_tomorrow = parse(start_time) <= parse(future_date[1]) <= parse(end_time)
        in_day_after = parse(start_time) <= parse(future_date[2]) <= parse(end_time)
        if in_today and not in_tomorrow:
            # 某个事件第二天结束
            event_end.append(event)
        elif not in_today and not in_tomorrow and in_day_after:
            # 后天开启的事件
            day_after_tomorrow_start.append(event)
        elif not in_today and in_tomorrow:
            # 明天开始事件
            tomorrow_start.append(event)
    tips = get_tips()
    message = "活动变更提示：\n"
    if event_end:
        message += "==========\n即将结束活动提示\n"
        for event in event_end:
            message += f"{event['name']}事件将于{event['end_time']}结束"
            if re.search(r"N图.*?|H图.*?", event['name']):
                message += "请各位指挥官确认装备或碎片是否都刷好刷满\n"
            elif re.search(r"公会战", event['name']):
                message += "今晚24点前记得一定要把公会战三刀出完喵~\n"
            elif re.search(r"露娜塔", event['name']):
                message += "本月的露娜塔活动要结束了，还请没打完的指挥官做好最后一击\n"
            elif re.search(r"活动.*?", event['name']):
                message += f"请各位指挥官记得清理剩余的boss券\n"
            else:
                message += f"还请指挥官多多注意喵~\n"
    if tomorrow_start:
        message += "=========\n明天开启活动提示\n"
        for event in tomorrow_start:
            if re.search(r"H图.*?", event['name']):
                message += f"明天将开启活动{event['name']},以下是拉菲为指挥官准备的计划：\n" + tips[1]
            else:
                message += f"明天{event['start_time']}将开启活动{event['name']},请各位指挥官做好准备\n"
    if day_after_tomorrow_start:
        message += "=========\n后天开启活动提示\n"
        for event in day_after_tomorrow_start:
            if re.search(r"N图.*?|H图.*?", event['name']):
                message += f"即将开启活动{event['name']},以下是拉菲为指挥官准备的计划：\n" + tips[0] + "\n"
            elif re.search(r"地下城.*?", event['name']):
                message += f"即将开启活动{event['name']},以下是拉菲为指挥官准备的计划：\n" + tips[2] + "\n"

    group_info = await bot.get_group_list()
    if event_end or day_after_tomorrow_start or tomorrow_start:
        for group in group_info:
            # group_list内容[{'group_id': , 'group_name': '', 'max_member_count': , 'member_count': }]
            await asyncio.sleep(0.5)
            await bot.send_group_msg(group_id=group['group_id'], message=message)
    else:
        return
