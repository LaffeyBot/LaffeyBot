from nonebot import on_command, CommandSession, permission as perm
from data.damage import delete_all_records, add_record
from pcr.plugins.record.alert_new_record import alert_new_record, boss_status_text
from data.json.json_editor import JSONEditor
from data.player_name import qq_to_game_name
import config
from pcr.plugins.get_best_name import get_best_name


@on_command('deleteAll', aliases='删除所有记录', only_to_me=True, permission=perm.SUPERUSER)
async def delete_all(session: CommandSession):
    delete_all_records()
    await session.send('已经把记录删掉了喵')


@on_command('manual_damage', aliases=['出刀', '报刀'], only_to_me=False)
async def manual_damage(session: CommandSession):
    if session.event.group_id != config.GROUP_ID:
        print('NOT IN SELECTED GROUP')
        return
    damage = session.get('damage')
    if not damage:
        await session.send('请输入伤害喵')
    username = get_best_name(session)
    game_name = qq_to_game_name(username)
    target = config.NAME_FOR_BOSS[JSONEditor().get_current_boss_order()-1]
    new_record, did_kill = add_record([[game_name, target, damage]], force=True)
    await alert_new_record(new_record, did_kill)


@on_command('status', aliases=['状态', 'boss状态'], only_to_me=False)
async def status(session: CommandSession):
    if session.event.group_id != config.GROUP_ID and session.event['message_type'] != 'private':
        print('NOT IN SELECTED GROUP')
        return
    editor = JSONEditor()
    message = '现在攻略的是' + str(editor.get_generation()) + '周目的' + \
              str(editor.get_current_boss_order()) + '王喵~\n'
    message += boss_status_text(editor.get_remaining_health())
    await session.send(message=message)


@manual_damage.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip().replace('出刀', '')

    if stripped_arg and stripped_arg.isdigit():
        session.state['damage'] = int(stripped_arg)
        return