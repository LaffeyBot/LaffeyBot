from utils import spider
import json


class TeamHomework(spider.Spiders):
    def parse(self) -> dict:
        response = self.doGet(**self.params)
        data = json.loads(response.text)
        return data

    def get_details(self, work_id: int) -> dict:
        params = {
            'target': 'get-gzlj-team-war-work-detail/a',
            'work_id': work_id
        }
        detail_url = 'https://www.bigfun.cn/api/feweb'
        self.change_url(detail_url)
        response = self.doGet(**params)
        detail_data = json.loads(response.text)
        return detail_data

    def get_pics(self):
        pass



if __name__ == '__main__':
    t = TeamHomework(
        'https://www.bigfun.cn/api/feweb?target=get-gzlj-team-war-work-list%2Fa&type=2&battle_id=3&boss_position=1&order=1&page=1')
    # t.parse()
    print(t.get_details(1357))
