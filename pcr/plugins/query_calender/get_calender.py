import requests
import json
import traceback
import logging


def calender_info() -> list:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
               'Content-Type': 'application/json;charset=utf-8',
               'Host':'tools.yobot.win'
               }
    url = 'https://tools.yobot.win/calender/cn.json'
    try:
        r = requests.get(url=url, headers=headers)
    except Exception as e:
        logging.error(traceback.format_exc())
        return ['指挥官您请求速度太快了，请稍后重试喵~']
    return json.loads(r.content.decode(), encoding='utf-8')


if __name__ == '__main__':
    print(calender_info())
    # print(type(calender_info()))
    from datetime import datetime
    from dateutil.parser import parse
    import datetime
    print(parse('2020/08/16 4:00:00')>=parse('2020/08/16 5:00:00'))
    threeDayAgo = datetime.datetime.today() - datetime.timedelta(3)
    print(threeDayAgo)
    otherStyleTime = threeDayAgo.strftime("%Y-%m-%d")
    print(otherStyleTime)
