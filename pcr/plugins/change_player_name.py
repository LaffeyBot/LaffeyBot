from nonebot import on_command, CommandSession, permission
from data.json.json_editor import JSONEditor
import config
from pcr.plugins.get_best_name import get_best_name
from data.init_database import get_connection
from data.player_name import qq_to_game_name


@on_command('change_player_name', aliases=['修改游戏名', '改名'], only_to_me=False, permission=permission.SUPERUSER)
async def change_player_name(session: CommandSession):
    group_id = session.event.group_id
    old_name = session.state['old_name']
    new_name = session.state['new_name']
    modify_name(old_name, new_name, group_id=group_id)
    await session.send(message='将' + old_name + '的游戏名修改为' + new_name + '了喵！')

    qq_id = session.event.user_id
    c = get_connection()
    cursor = c.cursor()
    cursor.execute('SELECT qq_name FROM player_list '
                   'WHERE group_id=%s AND qq_id=%s', (group_id, qq_id))
    old_qq_name = cursor.fetchone()
    new_qq_name = session.state['qq_name']
    if old_qq_name != new_qq_name:
        modify_qq_name(old_name, new_qq_name, group_id)
        await session.send(message='将' + old_qq_name + '的游戏名修改为' + new_qq_name + '了喵！')


def modify_name(old_name: str, new_name: str, group_id: int):
    c = get_connection()
    cursor = c.cursor()
    cursor.execute('UPDATE record SET username=%s '
                   'WHERE username=%s AND group_id=%s', (new_name, old_name, group_id))
    cursor.execute('UPDATE player_list SET player_name=%s '
                   'WHERE player_name=%s AND group_id=%s', (new_name, old_name, group_id))
    c.commit()


def modify_qq_name(old_name: str, new_name: str, group_id: int):
    c = get_connection()
    cursor = c.cursor()
    cursor.execute('UPDATE player_list SET qq_name=%s '
                   'WHERE qq_name=%s AND group_id=%s', (new_name, old_name, group_id))
    c.commit()


@change_player_name.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.replace('修改游戏名', '').strip()
    name: str = get_best_name(session)
    session.state['qq_name'] = name

    separated_args: list = stripped_arg.split(' ')
    if len(separated_args) > 1:
        # old_name new_name
        session.state['old_name'] = separated_args[0]
        session.state['new_name'] = separated_args[1]
    elif len(separated_args) == 1:
        # new_name
        player_name = qq_to_game_name(name, group_id=session.event.group_id)
        session.state['old_name'] = player_name
        session.state['new_name'] = separated_args[0]
