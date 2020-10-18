import requests
import random


class Spiders(object):
    def __init__(self, url='', params={}, data={}, **kwargs):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0']
        self.headers = {
            'User-Agent': user_agents[random.randint(0, len(user_agents) - 1)]
        }
        self.url = url
        if params:
            self.params = params
        if data:
            self.data = data

    def doGet(self, **kwargs):
        return requests.get(url=self.url, headers=self.headers, params=kwargs)

    def doPost(self, **kwargs):
        return requests.post(url=self.url, headers=self.headers, data=kwargs)

    def change_url(self, url):
        self.url = url

    def parse(self):
        pass
