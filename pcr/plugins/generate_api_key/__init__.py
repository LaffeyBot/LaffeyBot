import config
from nonebot import on_command, CommandSession, get_bot
import random
import string
from data.init_database import get_connection


@on_command('generate_api_key', aliases=('生成key',), only_to_me=False)
async def generate_api_key(session: CommandSession):
    if session.event.user_id not in config.SUPERUSERS:
        await session.send('权限不足喵...')

    else:
        api_key = get_random_string(16)
        group_id = session.event.group_id
        qq_id = session.event.user_id
        c = get_connection()
        cursor = c.cursor()
        cursor.execute('INSERT INTO api_keys (group_id, qq_id, api_key) VALUES '
                       '(%s, %s, %s)', (group_id, qq_id, api_key))
        c.commit()
        message = '这是指挥官的api_key：\n' + api_key + '\n请妥善保管喵~'
        await get_bot().send_private_msg(user_id=qq_id, message=message)
        await session.send('已经发送了api_key喵~')


def get_random_string(length: int) -> str:
    # Random string with the combination of lower and upper case
    charset = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(charset) for i in range(length))
    print(result_str)

    if get_connection().cursor().execute('SELECT * FROM api_keys '
                                         'WHERE api_key=%s', (result_str, )) != 0:
        # 如果已存在
        return get_random_string(length)

    return result_str
