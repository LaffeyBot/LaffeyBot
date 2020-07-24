from nonebot import on_command, CommandSession
import aiocqhttp
import nonebot


@on_command('add_group_members', aliases=['添加成员', '添加群成员', '更新群成员'], only_to_me=False)
async def list_attack_detail(session: CommandSession):
    group_id = session.event.group_id
    group_member_list = nonebot.get_bot().get_group_member_list(group_id=group_id)
    print(group_member_list)
