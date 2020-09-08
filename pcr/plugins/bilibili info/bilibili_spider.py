import re
import requests
import json
from bs4 import BeautifulSoup


class VideoInfo(object):
    def __init__(self,url: str):
        self.base_url = url
        self.api_url = 'https://api.bilibili.com/x/web-interface/archive/stat'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        }

    def get_video_info(self)->dict:
        result = re.search(r'https://www.bilibili.com/(.*?)/.*?',self.base_url)
        if result:
            video_type = result.group(1)
            if video_type == 'video':
                return self.get_ordinary_video_info()
        else:
            return {'code':601,'message':'url地址不是视频的地址'}

    def get_ordinary_video_info(self)->dict:
        # 获取视频编号，以便判断是av还是bv
        result = re.search(r'https://www.bilibili.com/video/(\w+)',self.base_url)
        self.headers['content-type'] = 'application/json; charset=utf-8'
        if result:
            num = result.group(1)
            if num.startswith('BV') or num.startswith('bv'):
                param = {'bvid':num}
                response = requests.get(url=self.api_url,headers=self.headers,params=param)
                print(type(json.loads(response.content.decode(), encoding='utf-8')))
                response_dic = json.loads(response.content.decode(), encoding='utf-8')
                temp = self.get_video_details()
                temp.update(response_dic)
                return temp
            elif num.startswith('AV') or num.startswith('av'):
                param = {'avid': num}
                response = requests.get(url=self.api_url, headers=self.headers, params=param)
                response_dic = json.loads(response.content.decode(), encoding='utf-8')
                temp = self.get_video_details()
                temp.update(response_dic)
                return temp
            else:
                return {'code':602,'message':'url格式不正确'}
        else:
            return {'code': 602, 'message': 'url格式不正确'}

    def get_video_details(self)->dict:
        response = requests.get(url=self.base_url,headers=self.headers)
        soup = BeautifulSoup(response.text,'lxml')
        result = {}
        print(soup.find(class_='info open').text)
        title_list = soup.find(attrs={'name': 'keywords','itemprop':'keywords'})['content'].split(',')
        result['title']= title_list[0]
        result['tags']= title_list[1:]
        result['author']=soup.find(attrs={'name': 'author','itemprop':'author'})['content']
        result['self_introduce'] = soup.find(class_='info open').text
        return result





if __name__ == '__main__':
    v = VideoInfo('https://www.bilibili.com/video/BV19f4y1173X/')
    print(v.get_video_info())