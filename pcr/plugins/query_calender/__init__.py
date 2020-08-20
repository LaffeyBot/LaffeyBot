from nonebot import on_command, CommandSession
from .get_calender import calender_info
from datetime import datetime
from dateutil.parser import parse
import datetime


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
        message += f'===={check_date.strftime("%Y{y}%m{m}%d{d}").format(y = "年",m = "月",d = "日")}====\n'
        if len(events) > 0:
            for event in events:
                message += f'>>{event}\n'
        else:
            message += '今日还暂时没有活动喵QAQ\n'

    message += '更多日程请查看：https://tools.yobot.win/calender/#cn'
    await session.send(message)
