import config
from nonebot import on_command, CommandSession
from aiocqhttp import MessageSegment
from data.picture_quota import PictureQuota
from data.init_database import get_connection
import time
import asyncio
import nonebot


@on_command('hentai', aliases=('炼铜', '瑟图', '色图', '本子', '涩图', '涩图'), only_to_me=False)
async def hentai(session: CommandSession):
    if session.event.group_id in config.GROUP_ID or session.event['message_type'] == 'private':
        user_id = session.event.sender['user_id']
        quota = PictureQuota(user_id)
        if not quota.get_one_picture():
            await session.send('指挥官要注意身体喵~')
            return

        cursor = get_connection().cursor()
        cursor.execute('SELECT * FROM picture_list ORDER BY RAND() LIMIT 1')
        random_file: (str, str, str) = cursor.fetchone()
        print(random_file)
        file_name = random_file[1] + '/' + random_file[0]
        print(file_name)
        seq = MessageSegment(type_='image', data={'file': file_name})
        if len(random_file[2]) > 0:
            message = '出处: ' + random_file[2]
            await session.send(message)
        # else:
        #     await hentai(session)
        #     return
        result = await session.send(seq)
        if int(time.strftime("%H", time.localtime())) < 14:
            asyncio.sleep(30)
            await session.bot.delete_msg(message_id=result['message_id'])
        bot = nonebot.get_bot()
        await bot.send_group_msg(group_id=session.event.group_id,
                                 message='[CQ:record,file=Laffey_voice\\Laffey_touch3.mp3]')
