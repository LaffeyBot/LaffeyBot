import nonebot
import re
import json
import requests
from aiocqhttp.event import Event
from .bilibili_spider import VideoInfo
bot = nonebot.get_bot()

@bot.on_message()
async def get_video_info(cq_event: Event):
    group_id = cq_event.group_id
    message = cq_event.message
    urls = re.findall(r'https?://www.bilibili.com\S+', str(message))
    # print('bilibili'+urls)
    if urls:
        for url in urls:
            await get_message(url,group_id)
    else:
        try:
            print(str(message))
            special_message = json.loads(str(message))
            # print(special_message['app'])
            if special_message['app'] == 'com.tencent.structmsg' and special_message['extra']['appid']==100951776:
                # 是bilibili旧版链接，不包含小程序
                print(special_message['meta']['news']['jumpUrl'])
                await get_message(special_message['meta']['news']['jumpUrl'],group_id)
            elif special_message['app'] == 'com.tencent.miniapp_01' and special_message['extra']['appid']==100951776:
                redirect_url = special_message['meta']['detail_1']['qqdocurl']
                response = requests.get(url=redirect_url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'})
                target_url = response.url
                await get_message(target_url,group_id)
        except Exception as e:
            print('其他类型数据，ignore')
            print(e)





async def get_message(url:str,group_id:int):
    msg = ''
    v = VideoInfo(url)
    result_dic = v.get_video_info()
    if result_dic['code'] == 0:
        msg += f'为指挥官查到{url.split("?")[0]}的视频简介如下：\n'
        msg += '视频标题是:' + result_dic['title'] + ' up是:' + result_dic['author'] + '\n'
        msg += '点赞数:' + str(result_dic['data']['like']) + ' 投币数:' + str(result_dic['data']['coin']) + ' 收藏数:' + \
               str(result_dic['data']['favorite']) + ' 分享数:' + str(result_dic['data']['share']) + '\n'
        msg += '当前播放数为:' + str(result_dic['data']['view']) + ' 弹幕数:' + str(result_dic['data']['danmaku']) + '\n'
        msg += '视频简介:\n' + result_dic['self_introduce']
        await bot.send_msg(group_id=group_id, message=msg)
    else:
        await bot.send_msg(group_id=group_id, message=result_dic['message'])