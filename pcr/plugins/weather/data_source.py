import requests
import json

url = "https://tianqiapi.com/api"
params_dic = {'appid': '23845672', 'appsecret': 'NhFIJ1tG', 'version': 'v6'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}


async def get_weather_of_city(city: str) -> str:
    params_dic['city'] = city
    params_dic['version']='v6'
    r = requests.get(url, headers=headers, params=params_dic)
    weather_dic = json.loads(r.content.decode(), encoding='utf8')
    if city != '北京' and weather_dic['city'] == '北京':
        return f'喵，{city}的天气暂时查不到喵QAQ'
    else:
        return '喵，指挥官所查询的城市{}当前天气情况为{},最低气温{},最高气温{},{}{},空气质量{}\n' \
               '茗喵小提示：{}'.format(weather_dic['city'], weather_dic['wea'], weather_dic['tem'],
                                 weather_dic['tem1'], weather_dic['win'], weather_dic['win_speed'],
                                 weather_dic['air_level'], weather_dic['air_tips'])


async def get_report(city: str) -> str:
    params_dic['version'] = 'v2'
    params_dic['city'] = city
    r = requests.get(url, headers=headers, params=params_dic)
    weather_dic = json.loads(r.content.decode(), encoding='utf8')
    if city != '北京' and weather_dic['city'] == '北京':
        return f'喵，{city}的天气暂时查不到喵QAQ'
    else:
        report = f'以下是{city}地区未来三天的天气预报喵~\n'
        for i in range(3):
            data_dict = weather_dic['data'][i + 1]
            report += '{}{},预计天气情况为{},其中白天为{},夜间为{},最高气温为{}°，最低气温为{}°\n'. \
                format(data_dict['date'], data_dict['week'], data_dict['wea'], data_dict['wea_day'],
                       data_dict['wea_night'], data_dict['tem1'], data_dict['tem2'])
        return report


if __name__ == '__main__':
    url = "https://tianqiapi.com/api"
    params_dic = {'appid': '23845672', 'appsecret': 'NhFIJ1tG', 'version': 'v2'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}
    r = requests.get(url, headers=headers, params=params_dic)
    print(json.loads(r.content.decode(), encoding='utf8'))
