from nonebot import on_command, CommandSession, permission as perm
from data.damage import delete_all_records, add_record
from pcr.plugins.manage_record.alert_new_record import alert_new_record, boss_status_text
from data.json.json_editor import JSONEditor
from data.player_name import qq_to_game_name
import config
from pcr.plugins.get_best_name import get_best_name
from data.model import *
from nonebot import get_bot


@on_command('deleteAll', aliases='删除所有记录', only_to_me=True, permission=perm.SUPERUSER)
async def delete_all(session: CommandSession):
    delete_all_records(session.event.group_id)
    await session.send('已经把记录删掉了喵')


@on_command('manual_damage', aliases=['出刀', '报刀'], only_to_me=False)
async def manual_damage(session: CommandSession):
    db.init_app(get_bot().server_app)
    group_id = session.event.group_id
    user: User = User.query.filter_by(qq=session.event.user_id).first()

    damage = session.get('damage')
    if not damage:
        await session.send('请输入伤害喵')

    new_record, did_kill = add_record([[game_name, target, damage]],
                                      force=True, group_id=group_id)
    await alert_new_record(new_record, did_kill, group_id=group_id)


@on_command('status', aliases=['状态', 'boss状态'], only_to_me=False)
async def status(session: CommandSession):
    editor = JSONEditor(group_id=session.event.group_id)
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
