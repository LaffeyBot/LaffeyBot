from nonebot import on_command, CommandSession, permission
from data.json.json_editor import JSONEditor
import config
from pcr.plugins.get_best_name import get_best_name
from data.init_database import get_connection
from data.player_name import qq_to_game_name


@on_command('change_player_name', aliases=['修改游戏名'], only_to_me=False, permission=permission.SUPERUSER)
async def change_player_name(session: CommandSession):
    if session.event.group_id != config.GROUP_ID and session.event['message_type'] != 'private':
        print('NOT IN SELECTED GROUP')
        return
    old_name = session.state['old_name']
    new_name = session.state['new_name']
    modify_name(old_name, new_name)
    await session.send(message='将' + old_name + '的名字修改为' + new_name + '了喵！')


def modify_name(old_name: str, new_name: str):
    c = get_connection()
    c.execute('UPDATE record SET username=? WHERE username=?', (new_name, old_name))
    c.execute('UPDATE player_list SET player_name=? WHERE player_name=?', (new_name, old_name))
    c.commit()


@change_player_name.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.replace('修改游戏名', '').strip()

    separated_args: list = stripped_arg.split(' ')
    if len(separated_args) > 1:
        # old_name new_name
        session.state['old_name'] = separated_args[0]
        session.state['new_name'] = separated_args[1]
    else:
        # new_name
        name: str = get_best_name(session)
        player_name = qq_to_game_name(name)
        session.state['old_name'] = player_name
        session.state['new_name'] = separated_args[0]
