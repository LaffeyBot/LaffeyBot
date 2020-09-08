import nonebot
import re
from aiocqhttp.event import Event
from .bilibili_spider import VideoInfo
bot = nonebot.get_bot()

@bot.on_message()
async def get_video_info(cq_event: Event):
    group_id = cq_event.group_id
    message = cq_event.message
    urls = re.findall('https://www.bilibili.com\S+', message)
    print(urls)
    if urls:
        for url in urls:
            msg = ''
            v = VideoInfo(url)
            result_dic = v.get_video_info()
            msg += f'为指挥官查到{url}的视频简介如下：\n'
            msg += '视频标题是:'+ result_dic['title']+' up是:'+ result_dic['author']+'\n'
            msg += '点赞数:'+ result_dic['data']['like']+' 投币数:'+result_dic['data']['coin']+' 收藏数:'+\
                   result_dic['data']['favorite']+' 分享数:'+result_dic['data']['share']+'\n'
            msg += '当前播放数为:'+result_dic['data']['view']+' 弹幕数:'+result_dic['data']['danmaku']+'\n'
            msg += '视频简介:\n'+result_dic['self_introduce']
            bot.send_group_msg(group_id=group_id,message=msg)

