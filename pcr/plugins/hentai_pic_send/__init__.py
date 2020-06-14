import config
from nonebot import on_command, CommandSession
from aiocqhttp import MessageSegment
from data.picture_quota import PictureQuota
from data.init_database import get_connection
import time


@on_command('hentai', aliases=('炼铜', '瑟图', '色图', '本子'), only_to_me=False)
async def hentai(session: CommandSession):
    if session.event.group_id == config.GROUP_ID or session.event['message_type'] == 'private':
        if int(time.strftime("%H", time.localtime())) < 14:
            await session.send('指挥官要好好休息喵~')
            return
        user_id = session.event.sender['user_id']
        quota = PictureQuota(user_id)
        if not quota.get_one_picture():
            await session.send('指挥官要注意身体喵~')
            return

        random_file: (str, str, str) = get_connection()\
            .execute('SELECT * FROM picture_list ORDER BY RANDOM() LIMIT 1').fetchone()
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
        await session.send(seq)
