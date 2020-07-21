from .service import Service, sucmd
import nonebot
from .log import new_logger
import config

logger = new_logger('hoshino', True)


def get_bot():
    return nonebot.get_bot()


def get_self_ids():
    bot = nonebot.get_bot()
    return bot._wsr_api_clients.keys()
