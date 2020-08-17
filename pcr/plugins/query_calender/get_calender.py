import requests
import json
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
           'Content-Type': 'application/json;charset=utf-8',
           }
url = 'https://tools.yobot.win/calender/cn.json'
r= requests.get(url=url,headers=headers)
def celender_info(r:requests)->dict:
    

if __name__ == '__main__':
    print(json.loads(r.content.decode(),encoding='utf-8'))
