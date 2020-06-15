from nonebot import on_command, CommandSession, permission as perm
from data.picture_quota import PictureQuota


@on_command('reset_quota', aliases='重设图片限制', only_to_me=False, permission=perm.SUPERUSER)
async def reset_quota(session: CommandSession):
    PictureQuota().clear_quota()
    await session.send('重设成功了喵~')
