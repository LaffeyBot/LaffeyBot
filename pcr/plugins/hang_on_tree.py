from nonebot import on_command, CommandSession
from data.json.json_editor import JSONEditor
import config


@on_command('hang_on_tree', aliases=['挂树'], only_to_me=False)
async def hang_on_tree(session: CommandSession):
    if session.event.group_id != config.GROUP_ID:
        print('NOT IN SELECTED GROUP')
        return
    name: str = session.event.sender['nickname']
    JSONEditor().add_on_tree(name)
    await session.send(message='将' + name + '挂到树上了喵~')

