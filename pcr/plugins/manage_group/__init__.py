from nonebot import on_command, CommandSession
from nonebot import on_notice, NoticeSession

group_id = [1104038724, 1108319335]
@on_notice('group_increase')
async def _(session: NoticeSession):
    if session.event.group_id in group_id:
        print(session.event.user_id)
        await session.send(f"欢迎新人@{session.event.sender['nickname']}加入一起py喵~")
