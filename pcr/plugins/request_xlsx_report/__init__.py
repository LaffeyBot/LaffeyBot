from nonebot import on_command, CommandSession
from data.init_database import get_connection
from aiocqhttp import MessageSegment
from datetime import datetime
import config
import os
from pcr.plugins.auth_tools import get_auth_header
import requests
import config


@on_command('request_xlsx_report', aliases=('获取出刀报告',), only_to_me=True)
async def request_xlsx_report(session: CommandSession):
    header = get_auth_header(for_qq=session.event.user_id)
    url = config.BACKEND_URL + '/v1/generate_report/generate'
    r = requests.get(url, headers=header)
    await session.send(r.json()['url'])
