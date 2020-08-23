import requests
import json


class SpiderTeamRank(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                        'Referer': 'https://kengxxiao.github.io/Kyouka/',
                        'Custom-Source': 'KyoukaOfficial',
                        'Content-Type': 'application/json;charset=utf-8',
                        }
        self.base_url = 'https://service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com'
        self.data = {}

    def get_team_rank_info_by_tname(self, team_name: str, time_stamp: int = 0) -> dict:
        # 给出公会名称和时间戳进行查询，时间戳指定了查询哪期会战
        if time_stamp == 0:
            self.data = {'history': 0, 'clanName': team_name}
        else:
            self.data = {'history': time_stamp, 'clanName': team_name}
        url = self.base_url + '/name/0'
        re = requests.post(url=url, headers=self.headers, json=self.data)
        print(re.json())
        return re.json()

    def get_team_rank_info_by_rank(self, team_rank: int = 1, time_stamp: int = 0) -> dict:
        if time_stamp == 0:
            self.data = {'history': 0}
        else:
            self.data = {'history': time_stamp}
        url = self.base_url + f'/rank/{team_rank}'
        re = requests.post(url=url, headers=self.headers, json=self.data)
        return json.loads(re.content.decode(), encoding='utf-8')

    def get_team_rank_info_by_leader(self, leader: str, time_stamp: int = 0) -> dict:
        if time_stamp == 0:
            self.data = {'history': 0, 'leaderName': leader}
        else:
            self.data = {'history': time_stamp, 'leaderName': leader}
        url = self.base_url + '/leader/0'
        re = requests.post(url=url, headers=self.headers, json=self.data)
        return json.loads(re.content.decode(), encoding='utf-8')

    def get_team_rank_info_by_score(self, score: int = 0, time_stamp: int = 0) -> dict:
        if time_stamp == 0:
            self.data = {'history': 0}
        else:
            self.data = {'history': time_stamp}
        url = self.base_url + f'/score/{score}'
        re = requests.post(url=url, headers=self.headers, json=self.data)
        return json.loads(re.content.decode(), encoding='utf-8')


if __name__ == '__main__':
    s = SpiderTeamRank()
    r = s.get_team_rank_info_by_rank(2333, 1591945200)
    r1 = s.get_team_rank_info_by_tname('碧蓝航线天下第一', 1591945200)
    r2 = s.get_team_rank_info_by_leader('^雨宫$')
    r3 = s.get_team_rank_info_by_tname('雨落的农场')
    print(r)
    print(r1)
    print(r2)
    print(r3)
