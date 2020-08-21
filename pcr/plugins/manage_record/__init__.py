from nonebot import on_command, CommandSession, permission as perm
from data.damage import delete_all_records, add_record
from pcr.plugins.manage_record.alert_new_record import boss_status_text
from data.json.json_editor import JSONEditor
from pcr.plugins.direct_send_message import send_from_dict


@on_command('deleteAll', aliases='删除所有记录', only_to_me=True, permission=perm.SUPERUSER)
async def delete_all(session: CommandSession):
    delete_all_records(session.event.group_id)
    await session.send('已经把记录删掉了喵')


@on_command('manual_damage', aliases=['出刀', '报刀'], only_to_me=False)
async def manual_damage(session: CommandSession):
    damage = session.get('damage')
    if not damage:
        await session.send('请输入伤害喵')

    await send_from_dict(
        add_record(qq=session.event.user_id, damage=int(damage), type_='normal')
    )


@on_command('last_damage', aliases=['尾刀'], only_to_me=False)
async def last_damage(session: CommandSession):
    await send_from_dict(
        add_record(qq=session.event.user_id, type_='last')
    )


@on_command('compensation_damage', aliases=['补偿刀'], only_to_me=False)
async def compensation_damage(session: CommandSession):
    damage = session.get('damage')
    if not damage:
        await session.send('请输入伤害喵')

    await send_from_dict(
        add_record(qq=session.event.user_id, damage=int(damage), type_='compensation')
    )


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
