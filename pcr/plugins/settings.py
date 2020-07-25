from nonebot import on_command, CommandSession, permission as perm
from data.damage import delete_all_records
from data.json.json_editor import JSONEditor


@on_command('stop_fetching', aliases='停止抓取', only_to_me=True, permission=perm.SUPERUSER)
async def stop_fetching(session: CommandSession):
    JSONEditor(session.event.group_id).set_fetch_status(False)
    await session.send('停止抓取了喵~')


@on_command('start_fetching', aliases='开始抓取', only_to_me=True, permission=perm.SUPERUSER)
async def start_fetching(session: CommandSession):
    JSONEditor(session.event.group_id).set_fetch_status(True)
    await session.send('开始抓取了喵~')
