from nonebot import get_bot


async def send_direct_message(type_: str, message: str, id_: int):
    if type_ == 'group':
        await get_bot().send_group_msg(group_id=id_, message=message)
    elif type_ == 'private':
        await get_bot().send_private_msg(user_id=id_, message=message)


async def send_from_dict(data: dict):
    await send_direct_message(type_=data['type'], message=data['message'], id_=data['id'])
