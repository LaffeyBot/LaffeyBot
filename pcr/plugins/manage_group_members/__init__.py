from nonebot import on_command, CommandSession
from data import init_database
import nonebot
import config
from data.user import User


@on_command('add_group_members', aliases=['添加成员', '添加群成员', '更新群成员'], only_to_me=False)
async def add_group_members(session: CommandSession):
    group_id = session.event.group_id
    bot = nonebot.get_bot()
    group_member_list = await bot.get_group_member_list(group_id=group_id)

    c = init_database.get_connection()
    cursor = c.cursor()
    cursor.execute('DELETE FROM player_list WHERE group_id=%s', (group_id,))
    c.commit()
    member_str = ''
    for member in group_member_list:
        qq_id = member['user_id']
        if qq_id == config.SELF_ID:
            continue
        qq_name = member['card']
        if len(qq_name) == 0:
            qq_name = member['nickname']
            member_str += qq_name + ', '

        role = member.get('role', 'member')
        cursor.execute('INSERT INTO player_list (group_id, qq_id, qq_name, player_name, role) '
                       'VALUES (%s, %s, %s, %s, %s)',
                       (group_id, qq_id, qq_name, qq_name, role))
    print(group_member_list)
    c.commit()
    await session.send('公会成员更新完成了喵~\n'
                       '当前成员：' + member_str)


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
