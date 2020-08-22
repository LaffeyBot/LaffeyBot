from nonebot import on_command, CommandSession
from data import init_database
import nonebot
import config
from nonebot.command.argfilter import extractors, validators
from data.model import *
from pcr.plugins.auth_tools import password_for
from datetime import datetime
from nonebot import get_bot


@on_command('add_group_members', aliases=['添加成员', '添加群成员', '更新群成员'], only_to_me=False)
async def add_group_members(session: CommandSession):
    db.init_app(get_bot().server_app)
    group_id = session.event.group_id
    group = Group.query.filter_by(group_chat_id=group_id).first()
    if not group:
        await session.send('本群还没有建立公会喵...')
        return
    bot = nonebot.get_bot()
    group_member_list = await bot.get_group_member_list(group_id=group_id)
    group_member_list.sort(key=take_qq_id)  # 必须排序以确保次序一致

    member_list_msg = '下面是本群成员列表喵：\n'
    for index, member in enumerate(group_member_list):
        qq_id, qq_name = get_id_and_name(member)
        if qq_id == config.SELF_ID:
            continue  # 排除自己

        member_list_msg += str(index) + '. '
        member_list_msg += qq_name + '\n'

    member_list_msg += '请输入不需要加入公会的成员序号，以空格隔开。如果没有请回复【无】喵。'
    exclusion_list: str = session.get(
        'exclusion_list', prompt=member_list_msg,
        arg_filters=[
            extractors.extract_text,  # 取纯文本部分
            str.strip,  # 去掉两边空白字符
            validators.match_regex('[0-9 无]+', '格式好像不对，请重新输入喵...')
        ]
    )
    exclusions = exclusion_list.split()

    member_str = ''
    for index, member in enumerate(group_member_list):
        qq_id, qq_name = get_id_and_name(member)
        if qq_id == config.SELF_ID or str(index) in exclusions:
            continue
        member_str += qq_name + ', '

    confirm_message = '当前成员：' + member_str + '\n'
    confirm_message += '确认要添加这些成员吗？请回复【确认】或【取消】喵'
    confirmation: str = session.get(
        'confirmation', prompt=confirm_message,
        arg_filters=[
            extractors.extract_text,  # 取纯文本部分
            str.strip,  # 去掉两边空白字符
        ]
    )

    if confirmation != '确认':
        await session.send('取消添加成员了喵...')
        return
    else:
        for index, member in enumerate(group_member_list):
            qq_id, qq_name = get_id_and_name(member)
            if qq_id == config.SELF_ID or str(index) in exclusions:
                continue
            existing_user = User.query.filter_by(qq=qq_id).first()
            if existing_user and existing_user.role >= 0:
                continue
            new_user: User = User(username=('temp_qq_' + str(qq_id)),
                                  nickname=qq_name,
                                  role=0,
                                  password=password_for(qq_id),
                                  created_at=datetime.now(),
                                  email='',
                                  email_verified=False,
                                  phone_verified=False,
                                  valid_since=datetime.now(),
                                  group_id=group.id,
                                  qq=qq_id,
                                  is_temp=True)
            db.session.add(new_user)
        db.session.commit()

        result_message = '已添加成员。\n' + '当前成员：' + member_str + '\n'
        await session.send(result_message)






def take_qq_id(elem):
    return elem['user_id']


def get_id_and_name(member) -> (int, str):
    qq_id: int = member['user_id']
    qq_name = member['card']
    if len(qq_name) == 0:
        qq_name = member['nickname']
    return qq_id, qq_name


@on_command('list_group_members', aliases=['公会成员', '成员列表'], only_to_me=False)
async def add_group_members(session: CommandSession):
    group_id = session.event.group_id

    c = init_database.get_connection()
    cursor = c.cursor()
    cursor.execute('SELECT * FROM player_list WHERE group_id=%s', (group_id,))
    message = '下面是当前的公会成员喵：\n'
    for index, member_record in enumerate(cursor.fetchall(), start=1):
        member = User(member_record)
        message += str(index) + '. ' + member.qq_name
        message += '，游戏名：' + member.player_name
        message += '，id: ' + member.id + '\n'

    message += '可以通过【踢出 id】指令来删除不在公会的成员喵~'
    await session.send(message)


@on_command('delete_group_members', aliases=['删除成员', '删除群成员', '提出群成员', '踢出'], only_to_me=False)
async def delete_group_members(session: CommandSession):
    group_id = session.event.group_id

    c = init_database.get_connection()
    cursor = c.cursor()

    to_delete = session.state['id_list']
    success_list = fail_list = []

    result = cursor.execute('DELETE FROM player_list '
                            'WHERE group_id=%s AND ', (group_id, ))
    c.commit()
    member_str = ''


@delete_group_members.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    id_list = []
    for arg in stripped_arg.split(' '):
        if arg.isdigit():
            id_list.append(arg)

    session.state['id_list'] = id_list
