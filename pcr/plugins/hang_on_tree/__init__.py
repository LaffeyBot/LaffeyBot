from nonebot import on_command, CommandSession
from data.json.json_editor import JSONEditor
import config
from pcr.plugins.get_best_name import get_best_name


@on_command('hang_on_tree', aliases=['挂树', '上树'], only_to_me=False)
async def hang_on_tree(session: CommandSession):
    if session.event.group_id not in config.GROUP_ID:
        print('NOT IN SELECTED GROUP')
        return
    name: str = get_best_name(session)
    JSONEditor().add_on_tree(name)
    await session.send(message='将' + name + '挂到树上了喵~')


@on_command('release_from_tree', aliases=['下树'], only_to_me=False)
async def release_from_tree(session: CommandSession):
    if session.event.group_id not in config.GROUP_ID:
        print('NOT IN SELECTED GROUP')
        return
    name: str = get_best_name(session)
    JSONEditor().remove_from_tree(name)
    await session.send(message='将' + name + '从树上放下来了喵~')
