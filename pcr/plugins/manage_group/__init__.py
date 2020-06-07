from nonebot import on_command, CommandSession
from nonebot import on_notice, NoticeSession
import config
from .send_email import email

#group_id = [1104038724, 1108319335]
@on_notice('group_increase')
async def welcome_new_member(session: NoticeSession):
    # 群成员增加时自动触发欢迎信息功能
    if session.event.group_id == config.GROUP_ID:
        print(session.event)
        await session.send(f"欢迎新的指挥官@{session.event.user_id}加入碧蓝焊接指挥部喵~\n"
                           + config.WELCOME_MESSAGE)


@on_command('feedback', aliases=('bug反馈', '功能反馈'), only_to_me=False)
async def feedback_bugs(session: CommandSession):
    # 反馈bug/建议，会自动向config.py文件中配置的开发者邮箱发送email
    if session.event.group_id != config.GROUP_ID:
        print('NOT IN SELECTED GROUP')
        return
    bug_info = session.get('bug_info', prompt="请问指挥官有什么bug或者新的功能需求需要反馈的喵？>_<")
    print(session.event)
    print(bug_info)
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










