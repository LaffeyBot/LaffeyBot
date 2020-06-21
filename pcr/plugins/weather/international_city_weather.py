import xlrd
import os
import config
import requests
import json
from .city_quota import Position

file_name1 = 'adcode-release-2020-06-10.xls'
file_name2 = 'globalcities.xls'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}
params_dic = {'lang':'zh_CN'}

def get_detail_city_weather_report(city):
    p1 = Position(file_name1)
    p2 = Position(file_name2)
    if p1.is_exist_city(city)[0]:
        # 国内城市
        position_ls=p1.get_position(city)
        url = f'https://api.caiyunapp.com/v2.5/Ex10EgS9FbyQg1nh/{position_ls[0]},{position_ls[1]}/weather.json'
        message=get_data(url)

    else:
        # 国外主要城市
        position_ls = p2.get_position(city)
        url = f'https://api.caiyunapp.com/v2.5/Ex10EgS9FbyQg1nh/{position_ls[1]},{position_ls[0]}/weather.json'
        message=get_data(url)
    if message:
        return message
    else:
        return '喵，没有找到指挥官想要查询城市的天气信息的说喵QAQ'

def get_data(url):

    r= requests.get(url,headers=headers,params=params_dic)
    weather_dic = json.loads(r.content.decode(), encoding='utf8')
    print(url)
    print(weather_dic)
    current_temperature= weather_dic['result']['realtime']['temperature']
    current_air = weather_dic['result']['realtime']['air_quality']['description']['usa']
    future_weather_minute = weather_dic['result']['minutely']['description']
    future_weather_hour = weather_dic['result']['hourly']['description']
    result = f'喵，指挥官查询的城市天气情况如下：\n' \
             f'当前气温为{current_temperature}℃,空气质量为{current_air}\n' \
             f'未来几小时的天气情况概述：{future_weather_minute}\n' \
             f'未来24小时天气情况概述：{future_weather_hour}\n'
    return result








if __name__ == '__main__':
    print(os.path.join(config.PROJECT_PATH,'adcode-release-2020-06-10.xls'))
    file_path = os.path.join(config.PROJECT_PATH,'adcode-release-2020-06-10.xls')
    excel = xlrd.open_workbook(file_path,encoding_override='utf8')
    all_sheet = excel.sheets()
    print(all_sheet)
    for i in all_sheet:
        print(i.name)
        print(i.nrows)
        print(i.ncols)
        for j in range(i.nrows):
            if j<10:
                print(i.row_values(j))
    print('====')
    get_data(116.4074,39.9042)
