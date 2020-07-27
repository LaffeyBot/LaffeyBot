from nonebot import on_command, CommandSession
import config


@on_command('self_introduction', aliases=['自我介绍', '来做个自我介绍'], only_to_me=False)
async def self_introduction(session: CommandSession):
    if session.event.group_id not in config.PRIMARY_GROUP_ID and session.event['message_type'] != 'private':
        print('NOT IN SELECTED GROUP')
        return
    await session.send(config.SELF_INTRODUCTION)
