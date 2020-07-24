from nonebot import on_command, CommandSession
from data import init_database
import nonebot


@on_command('add_group_members', aliases=['添加成员', '添加群成员', '更新群成员'], only_to_me=False)
async def list_attack_detail(session: CommandSession):
    group_id = session.event.group_id
    bot = nonebot.get_bot()
    group_member_list = await bot.get_group_member_list(group_id=group_id)

    c = init_database.get_connection()
    cursor = c.cursor()
    cursor.execute('DELETE FROM player_list WHERE group_id=%s', (group_id,))
    c.commit()
    for member in group_member_list:
        qq_id = member['user_id']
        qq_name = member['card']
        if len(qq_name) == 0:
            qq_name = member['nickname']
            cursor.execute('INSERT INTO player_list (group_id, qq_id, qq_name, player_name) '
                           'VALUES (%s, %s, %s, %s)', (group_id, qq_id, qq_name, qq_name))
    print(group_member_list)
    await session.send('公会成员更新完成了喵~')
