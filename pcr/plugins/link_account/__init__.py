from nonebot import on_command, CommandSession
from data import init_database
import nonebot
import config
from data.user import User
from nonebot.command.argfilter import extractors, validators
from data.model import *
from pcr.plugins.auth_tools import password_for
from datetime import datetime
from nonebot import get_bot


@on_command('link_account', aliases=['绑定账户'], only_to_me=False)
async def link_account(session: CommandSession):
    pass

