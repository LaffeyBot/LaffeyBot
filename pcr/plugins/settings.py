from nonebot import on_command, CommandSession, permission as perm
from data.damage import delete_all_records
from data.json.json_editor import JSONEditor


@on_command('stop_fetching', aliases='停止抓取', only_to_me=False, permission=perm.SUPERUSER)
async def stop_fetching(session: CommandSession):
    group_id = session.event.group_id
    if not group_id or len(group_id) == 0:
        if session.event.user_id == 540349946:
            group_id = 967350580
        elif session.event.user_id == 353884697:
            group_id = 1043493394

    JSONEditor(group_id).set_fetch_status(False)
    await session.send('停止抓取了喵~')


@on_command('start_fetching', aliases='开始抓取', only_to_me=False, permission=perm.SUPERUSER)
async def start_fetching(session: CommandSession):
    group_id = session.event.group_id
    if not group_id or len(group_id) == 0:
        if session.event.user_id == 540349946:
            group_id = 967350580
        elif session.event.user_id == 353884697:
            group_id = 1043493394

    JSONEditor(group_id).set_fetch_status(True)
    await session.send('开始抓取了喵~')
