import requests
import json

# url = "https://service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com//name/0"
url = "https://service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com//rank/4816"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
           'Referer':'https://kengxxiao.github.io/Kyouka/',
           'Custom-Source':'KyoukaOfficial',
           'Content-Type':'application/json;charset=utf-8',
}
# data = {'history': 0, 'clanName': '碧蓝航线天下第一'}
data = {'history': 0}
re = requests.post(url=url,headers=headers,json=data)
if __name__ == '__main__':
    print(json.loads(re.content.decode(), encoding='utf8'))
    print(type(json.loads(re.content.decode(), encoding='utf8')))
