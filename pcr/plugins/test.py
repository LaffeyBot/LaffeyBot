from nonebot import on_command, CommandSession, permission as perm


@on_command('test', aliases='测试', only_to_me=False, permission=perm.SUPERUSER)
async def test(session: CommandSession):
    event = session.event
    print(session.event)
    response = '现在的group_id:' + str(event.group_id) + '\n' + \
               '内容: ' + event.raw_message + '\n' + \
               '发件人: ' + event.sender['nickname']
    await session.send(response)
