from nonebot import on_command, CommandSession
from data.json.json_editor import JSONEditor
import config
from pcr.plugins.get_best_name import get_best_name
from data.player_name import qq_to_game_name


@on_command('no_report', aliases=['停止播报', '停止汇报', '停止报告'], only_to_me=False)
async def no_report(session: CommandSession):
    if session.event.group_id != config.PRIMARY_GROUP_ID and session.event['message_type'] != 'private':
        print('NOT IN SELECTED GROUP')
        return
    name: str = get_best_name(session)
    game_name = qq_to_game_name(name)
    JSONEditor().add_to_no_report_list(game_name)
    await session.send(message='将不会再播报' + name + '的出击了喵~')


@on_command('do_report', aliases=['开始播报', '重新汇报', '开始报告', '开始汇报'], only_to_me=False)
async def do_report(session: CommandSession):
    if session.event.group_id != config.PRIMARY_GROUP_ID and session.event['message_type'] != 'private':
        print('NOT IN SELECTED GROUP')
        return
    name: str = get_best_name(session)
    game_name = qq_to_game_name(name)
    JSONEditor().remove_from_no_report_list(game_name)
    await session.send(message='将会播报' + name + '的出击了喵~')
