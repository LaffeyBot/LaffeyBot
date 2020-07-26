import nonebot
import config
import random as r
import os
import pytz
from datetime import datetime
from aiocqhttp.exceptions import Error as e


@nonebot.scheduler.scheduled_job('cron', hour='8-23/1')
async def send_hour_message():
    # 定时在群聊中发布消息，活跃群气氛
    bot = nonebot.get_bot()
    msg = config.LAFFEY_MESSAGE[r.randint(0, len(config.LAFFEY_MESSAGE) - 1)]
    time_msg = f'现在是北京时间{datetime.now().hour}点{datetime.now().minute}分\n'
    for group in config.GROUP_ID:
        try:
            if datetime.now().hour == 8 and datetime.now().minute == 0:
                await bot.send_group_msg(group_id=group, message="指挥官休息的还好吗，拉菲现在很有精神，大概")
            elif datetime.now().hour == 23 and datetime.now().minute == 30:
                await bot.send_group_msg(group_id=group, message="呼啊...指挥官，要一起睡一会儿吗？")
            else:
                await bot.send_group_msg(group_id=group, message=time_msg + msg)
        except e:
            print(e)
            await bot.send_group_msg(group_id=group, message="唔……嗯……糟了，站着睡着了")
        rls = os.listdir(r'C:\Users\david\Documents\酷Q_Pro\data\record\Laffey_voice')
        record_file= os.path.join(r'\Laffey_voice',
                                  rls[r.randint(0, len(rls) - 1)])
        await bot.send_group_msg(group_id=group,message=f'[CQ:record,file={record_file}]')



# @nonebot.scheduler.scheduled_job('cron', hour=23, minute=5)
# async def hint_message():
#     bot = nonebot.get_bot()
#     msg = "还有55分钟今天就要结束了喵，指挥官记得回港区查看今日任务都完成了没喵~"
#     for group
#     try:
#         await bot.send_group_msg(group_id=config.GROUP_ID, message=msg)
#     except e:
#         await bot.send_group_msg(group_id=config.GROUP_ID, message=e)


@nonebot.scheduler.scheduled_job('cron', hour=12, minute=15)
async def hint_message():
    bot = nonebot.get_bot()
    msg = "今天，等一下好像有什么事情要做的样子……唔，记不起来了……指挥官，一起午睡吗？"
    for group in config.GROUP_ID:
        try:
            await bot.send_group_msg(group_id=group, message=msg)
        except e:
            await bot.send_group_msg(group_id=group, message=e)

