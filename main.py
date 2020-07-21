import nonebot
import config
from os import path
from log import new_logger

logger = new_logger('bot', config.DEBUG)

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'pcr', 'plugins'),
        'pcr.plugins'
    )
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'pcr/plugins', 'priconne'),
        'pcr.plugins.priconne'
    )
    nonebot.run()
