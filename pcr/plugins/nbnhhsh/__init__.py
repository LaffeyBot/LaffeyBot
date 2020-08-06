from nbnhhsh.nbnhhsh import suo

from nonebot import on_command, CommandSession
import config


@on_command('nbnhhsh', aliases=('解码', '翻译'), only_to_me=False)
async def nbnhhsh(session: CommandSession):
    encoded_text = session.get('encoded_text', prompt='指挥官想要翻译什么喵？')
    try:
        decoded: str = suo(encoded_text)
        message = '可能的翻译是：\n' + decoded
        await session.send(message)
    except UnboundLocalError:
        await session.send('翻译不能喵...')


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
