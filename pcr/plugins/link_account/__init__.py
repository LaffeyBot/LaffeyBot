from nonebot import on_command, CommandSession
from server_app.auth_tools import get_user_with
from data.user import User
from nonebot.command.argfilter import extractors, validators
from data.model import *
from pcr.plugins.auth_tools import link_account_with
from datetime import datetime
from nonebot import get_bot


@on_command('link_account', aliases=['绑定账户'], only_to_me=True)
async def link_account(session: CommandSession):
    db.init_app(get_bot().server_app)
    account = session.state['account']

    current_account: User = User.query.filter_by(qq=session.event.user_id).first()
    if current_account and not current_account.is_temp:
        session.finish(message='本QQ号已经绑定了一个账户了喵...')

    account_to_link = get_user_with(username=account)
    if account_to_link is None:
        session.finish(message='没有找到相应的账户喵...')
    if account_to_link.qq is not None:
        session.finish(message=account + '已经绑定了一个QQ了喵...')

    confirm_message = '确定要绑定账户 ' + account + ' 吗？此操作将不能撤回喔。请回复【确认/取消】'
    confirmation: str = session.get(
        'confirmation', prompt=confirm_message,
        arg_filters=[
            extractors.extract_text,  # 取纯文本部分
            str.strip,  # 去掉两边空白字符
        ]
    )
    if confirmation == '确认':
        link_account_with(qq=session.event.user_id, account=account)
        session.finish(message='绑定成功了喵！')


@link_account.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip().replace('绑定账户', '').strip()

    if stripped_arg:
        session.state['account'] = stripped_arg
    else:
        session.finish(message='请使用【绑定账户 账户名】这样的格式喵')
