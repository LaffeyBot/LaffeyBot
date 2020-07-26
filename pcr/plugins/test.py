from nonebot import on_command, CommandSession, permission as perm, get_bot


@on_command('test', aliases='发送测试', only_to_me=False)
async def test(session: CommandSession):
    event = session.event
    print(session.event)
    response = '现在的group_id:' + str(event.group_id) + '\n' + \
               '内容: ' + event.raw_message + '\n' + \
               '发件人: ' + event.sender['nickname']
    if 'card' in event.sender:
        response += '\n 群名片：' + event.sender['card']
    await session.send(response)
    group_member_list = await get_bot().get_group_member_list(group_id=event.group_id)
    print(group_member_list)
