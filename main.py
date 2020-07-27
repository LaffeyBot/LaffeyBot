import nonebot
import config
import os
from log import new_logger
from nonebot import Message, MessageSegment, message_preprocessor
from nonebot.message import CanceledException

logger = new_logger('bot', config.DEBUG)

_bot = None
HoshinoBot = nonebot.NoneBot
os.makedirs(os.path.expanduser('~/.hoshino'), exist_ok=True)
logger = new_logger('hoshino', config.DEBUG)


def init() -> HoshinoBot:
    global _bot
    nonebot.init(config)
    _bot = nonebot.get_bot()
    _bot.finish = _finish

    from hoshino.log import error_handler, critical_handler
    nonebot.logger.addHandler(error_handler)
    nonebot.logger.addHandler(critical_handler)

    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        os.path.join(os.path.dirname(__file__), 'pcr', 'plugins'),
        'pcr.plugins'
    )
    nonebot.load_plugins(
        os.path.join(os.path.dirname(__file__), 'pcr/plugins', 'priconne'),
        'pcr.plugins.priconne'
    )

    from hoshino import msghandler

    return _bot


async def _finish(event, message, **kwargs):
    if message:
        await _bot.send(event, message, **kwargs)
    raise CanceledException('ServiceFunc of HoshinoBot finished.')


def get_bot() -> HoshinoBot:
    if _bot is None:
        raise ValueError('HoshinoBot has not been initialized')
    return _bot


def get_self_ids():
    return _bot._wsr_api_clients.keys()


from hoshino import R
from hoshino.service import Service, sucmd

if __name__ == '__main__':
    bot = init()
    from server_app import report_damage, do_fetch, report_rank
    bot.run()
