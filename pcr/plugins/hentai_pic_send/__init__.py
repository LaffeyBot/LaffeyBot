import config
from nonebot import on_command, CommandSession
from aiocqhttp import MessageSegment
from data.picture_quota import PictureQuota
from data.init_database import get_connection
import time
import asyncio
import nonebot
from hoshino.util import load_image_as_cqimage, load_recording_as_cqrecord


@on_command('hentai', aliases=('炼铜', '瑟图', '色图', '本子', '涩图', '涩图'), only_to_me=False)
async def hentai(session: CommandSession):
    user_id = session.event.sender['user_id']
    quota = PictureQuota(user_id)
    if not quota.get_one_picture():
        await session.send('指挥官要注意身体喵~')
        return

    cursor = get_connection().cursor()
    cursor.execute('SELECT * FROM picture_list ORDER BY RAND() LIMIT 1')
    random_file: (str, str, str) = cursor.fetchone()
    print(random_file)
    file_name = 'images/' + random_file[1] + '/' + random_file[0]
    print(file_name)
    cq_image = load_image_as_cqimage(file_name)
    if len(random_file[2]) > 0:
        cq_image += '\n出处: ' + random_file[2]
    # else:
    #     await hentai(session)
    #     return
    result = await session.send(cq_image)

    # bot = nonebot.get_bot()

    # recording_file = 'recordings/Laffey_voice/Laffey_touch3.mp3'
    # cqrecord = load_recording_as_cqrecord(recording_file)
    # await bot.send_group_msg(group_id=session.event.group_id,
    #                          message=cqrecord)
    if int(time.strftime("%H", time.localtime())) < 14:
        await asyncio.sleep(60)
        await session.bot.delete_msg(message_id=result['message_id'])
    '''bot = nonebot.get_bot()
        await bot.send_group_msg(group_id=session.event.group_id,
                                 message='[CQ:record,file=Laffey_voice\\Laffey_touch3.mp3]')'''
