from nonebot import on_command, CommandSession
from data import init_database
import nonebot


@on_command('add_group_members', aliases=['添加成员', '添加群成员', '更新群成员'], only_to_me=False)
async def list_attack_detail(session: CommandSession):
    group_id = session.event.group_id
    bot = nonebot.get_bot()
    group_member_list = await bot.get_group_member_list(group_id=group_id)

    c = init_database.get_connection()
    for member in group_member_list:
        qq_id = member['user_id']
        qq_name = member['card']
        if len(qq_name) == 0:
            qq_name = member['nickname']
        c.cursor().execute('INSERT INTO player_list ')
    print(group_member_list)
