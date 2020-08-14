from nbnhhsh.nbnhhsh import suo
import urllib
from nonebot import on_command, CommandSession
import requests
import hashlib
import random
import config


@on_command('nbnhhsh', aliases=('解码', '翻译'), only_to_me=False)
async def nbnhhsh(session: CommandSession):
    encoded_text = session.get('encoded_text', prompt='指挥官想要翻译什么喵？')
    try:
        decoded: str = suo(encoded_text)
        message = '可能的翻译是：\n' + decoded
        print(message)
        await session.send(message,at_sender=True)
        print(message)
        return
    except:
        result = translate(encoded_text)
        message = '可能的翻译是：\n' + result
        await session.send(message, at_sender=True)
        return


@nbnhhsh.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['encoded_text'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('格式：【翻译 y1s1】')

    session.state[session.current_key] = stripped_arg


def translate(srcString, appid=config.BAIDU_APP_ID, secret_key=config.BAIDU_SECRET_KEY, fromLang='auto', toLang='zh'):
    myurl = '/api/trans/vip/translate'
    q = srcString
    salt = random.randint(32768, 65536)

    sign = appid + q + str(salt) + secret_key
    m1 = hashlib.md5()
    print(sign)
    m1.update(sign.encode('utf-8'))
    sign = m1.hexdigest()
    myurl = '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' \
            + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    r = requests.get('https://fanyi-api.baidu.com/api/trans/vip/translate' + myurl)
    json_ = r.json()
    result = json_['trans_result'][0]['dst']
    return result
    return ''