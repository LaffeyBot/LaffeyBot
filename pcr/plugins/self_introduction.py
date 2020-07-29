from nonebot import on_command, CommandSession
import config


@on_command('self_introduction', aliases=['自我介绍', '来做个自我介绍'], only_to_me=False)
async def self_introduction(session: CommandSession):
    await session.send(config.SELF_INTRODUCTION)
