from nonebot import on_command, CommandSession
from nonebot import on_notice, NoticeSession
import config
from .send_email import email
import re
import nonebot
import asyncio


# group_id = [1104038724, 1108319335]
@on_notice('group_increase')
async def welcome_new_member(session: NoticeSession):
    # 群成员增加时自动触发欢迎信息功能
    if session.event.group_id == config.PRIMARY_GROUP_ID:
        print(session.event)
        await session.send(f"欢迎新的指挥官@{session.event.user_id}加入碧蓝焊接指挥部喵~\n"
                           + config.WELCOME_MESSAGE)


@on_command('feedback', aliases=('bug反馈', '功能反馈'), only_to_me=False)
async def feedback_bugs(session: CommandSession):
    # 反馈bug/建议，会自动向config.py文件中配置的开发者邮箱发送email
    if session.event.group_id in config.GROUP_ID:
        print('NOT IN SELECTED GROUP')
        return
    bug_info = session.get('bug_info', prompt="请问指挥官有什么bug或者新的功能需求需要反馈的喵？>_<")
    print(session.event)
    print(bug_info)
    if re.match(r'break', bug_info) is not None:
        await session.send('会话已经终止了喵~')
        return
    if session.event.sender['card']:
        status = email(session.event.sender['card'], bug_info)
        if status:
            await session.send("喵，已经成功通知了喵~")
        else:
            await session.send("QAQ喵，发送失败了喵，重新试试喵")
    else:
        status = email(session.event.sender['nickname'], bug_info)
        if status:
            await session.send("喵，已经成功通知了喵~")
        else:
            await session.send("QAQ喵，发送失败了喵，重新试试喵")

# bot = nonebot.get_bot()
# @bot.on_message()
# async def demo(event):
#     print("demo")
#     info = await bot.get_group_member_list(group_id=1043493394)
#     '''for i in info:
#         print(i)'''
#
#     if event['message_type']=='group' and event['group_id'] in config.GROUP_ID:
#         print('=')
#         print("event is:%s"%event)
#         print(event['sender']['nickname'])
#         if event['sender']['nickname']=='genres':
#             msg_id = await bot.send_group_msg(group_id=1108319335, message='oxo')
#             await asyncio.sleep(5)
#             print(msg_id['message_id'])
#             await bot.delete_msg(message_id=event['message_id'])
#     '''if event['message_type']=='private':
#         # msg_id = await bot.send_group_msg(group_id=594524346, message='oxo')
#         msg_id = await bot.send_private_msg(user_id=3551318424, message='oxo')
#         await asyncio.sleep(5)
#         print(msg_id['message_id'])
#         await bot.delete_msg(message_id=msg_id['message_id'],self_id=3473890852)
#         # await bot.delete_msg(**event)'''
