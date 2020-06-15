from nonebot import get_bot
from aiocqhttp.event import Event
from data.json.json_editor import JSONEditor

bot = get_bot()


@bot.on_message()
async def group(cq_event: Event):
    print(cq_event)
    if JSONEditor().do_repeat(cq_event):
        await bot.send(cq_event, cq_event.message)

