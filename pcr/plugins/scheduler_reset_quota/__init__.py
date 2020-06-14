import nonebot
import config
from data.picture_quota import PictureQuota


@nonebot.scheduler.scheduled_job('cron', hour='*/6')
async def send_hour_message():
    PictureQuota().clear_quota()
