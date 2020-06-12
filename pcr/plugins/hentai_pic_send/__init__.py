import config
from nonebot import on_command, CommandSession
from aiocqhttp import MessageSegment

@on_command('hentai', aliases=('炼铜', '瑟图', '色图', '本子'), only_to_me=False)
async def hentai(session: CommandSession):
    if session.event.group_id == config.GROUP_ID:

        name = session.get('name')
        print('xxxxx')
        seq = MessageSegment.image(r'D:\酷Q\酷Q Air\data\image\1.jpg')
        await session.send(seq)
