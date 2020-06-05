from nonebot import on_command, CommandSession
from nonebot import on_notice, NoticeSession
import config

#group_id = [1104038724, 1108319335]
@on_notice('group_increase')
async def welcome_new_member(session: NoticeSession):
    # 群成员增加时自动触发欢迎信息功能
    if session.event.group_id != config.GROUP_ID and session.event['message_type'] != 'private':
        print(session.event.user_id)
        if session.event.sender['card'] != '':
            await session.send(f"欢迎新的指挥官@{session.event.sender['card']}加入碧蓝焊接指挥部喵~\n"
                               + config.WELCOME_MESSAGE)
        else:
            await session.send(f"欢迎新的指挥官@{session.event.sender['nickname']}加入碧蓝焊接指挥部喵~\n"
                               + config.WELCOME_MESSAGE)

