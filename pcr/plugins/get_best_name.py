from nonebot import CommandSession


def get_best_name(session: CommandSession):
    username = session.event.sender['nickname']
    if 'card' in session.event.sender and len(session.event.sender['card']) > 0:
        username = session.event.sender['card']
    return username
