from nonebot import on_command, CommandSession
from nonebot import on_notice, NoticeSession
import config
from .send_email import email
import re
import nonebot
import asyncio
from nonebot.command.argfilter import extractors, validators
from data.model import *


# group_id = [1104038724, 1108319335]
@on_notice('group_increase')
async def welcome_new_member(session: NoticeSession):
    # 群成员增加时自动触发欢迎信息功能
    print(session.event)
    await session.send(f"欢迎新的指挥官@{session.event.user_id}加入群喵~\n"
                       + config.WELCOME_MESSAGE)


@on_command('feedback', aliases=('bug反馈', '功能反馈'), only_to_me=False)
async def feedback_bugs(session: CommandSession):
    # 反馈bug/建议，会自动向config.py文件中配置的开发者邮箱发送email
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


@on_command('create_group', aliases=('创建公会', '创立公会'), only_to_me=False)
async def create_group(session: CommandSession):
    if Group.query.filter_by(group_chat_id=str(session.event.group_id)).first():
        await session.send('本群已经有一个公会了喵...')
        return
    current_user: User = User.query.filter_by(qq=session.event.user_id).first()
    if not current_user:
        await session.send('公会创建者必须有一个账号喵...')

    group_name = session.get('group_name', prompt='公会的名称是什么呢喵？',
                             arg_filters=[
                                 extractors.extract_text,  # 取纯文本部分
                                 str.strip,  # 去掉两边空白字符
                             ])
    new_group = Group(group_chat_id=str(session.event.group_id),
                      name=group_name)
    db.session.add(new_group)
    db.session.commit()
    db.session.refresh(new_group)
    current_user.group_id = new_group.id
    current_user.role = 2


bot = nonebot.get_bot()


@bot.on_message()
async def demo(event):
    if event['message_type'] == 'group' and event['group_id'] in config.GROUP_ID:
        print("demo2")
        # await bot.send_group_msg(group_id=1108319335, message='[CQ:record,file=Laffey_introduce.mp3]')
