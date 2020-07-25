from nonebot import get_bot
from aiocqhttp.event import Event
from data.json.json_editor import JSONEditor

bot = get_bot()


@bot.on_message()
async def group(cq_event: Event):
    group_id = cq_event.group_id
    if JSONEditor(group_id).do_repeat(cq_event):
        await bot.send(cq_event, cq_event.message)

