from nonebot import on_command, CommandSession, permission as perm
from pcr.plugins.auth_tools import get_auth_header
import requests
import config


@on_command('stop_fetching', aliases='停止抓取', only_to_me=False)
async def stop_fetching(session: CommandSession):
    qq = session.event.user_id
    auth_header = get_auth_header(for_qq=qq)
    url = config.BACKEND_URL + '/v1/user/set_ocr_status'
    json = dict(status=False, origin='QQ')
    r = requests.post(url=url, json=json, headers=auth_header)
    if r.status_code == 200:
        await session.send('停止抓取了喵~如需开始抓取请发送【开始抓取】')
    else:
        await session.send(str(r.text))


@on_command('start_fetching', aliases='开始抓取', only_to_me=False)
async def start_fetching(session: CommandSession):
    print('IS_FETCHING')
    qq = session.event.user_id
    auth_header = get_auth_header(for_qq=qq)
    url = config.BACKEND_URL + '/v1/user/set_ocr_status'
    json = dict(status=True, origin='QQ')
    r = requests.post(url=url, json=json, headers=auth_header)
    if r.status_code == 200:
        await session.send('开始抓取了喵~')
    else:
        await session.send(str(r.text))
