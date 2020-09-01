from bs4 import BeautifulSoup
import requests
import os
import config
import json


class Wiki(object):
    def __init__(self):
        # wiki角色主页地址
        self.base_url = 'https://wiki.biligame.com/pcr/%E8%A7%92%E8%89%B2%E5%9B%BE%E9%89%B4'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}

    def get_soup_by_net(self, url: str) -> BeautifulSoup:
        response = requests.get(url=url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    def get_role_gifs(self) -> list:
        soup = self.get_soup_by_net(self.base_url)
        # 获取所有角色的a标签 这个select内容可能需要随着wiki页面改动而修改
        targets = soup.select('.resp-tabs-container>.resp-tab-content>.box-js a')
        name = []

        for target in targets:
            role_name = target['title']
            name.append(role_name)
            dir_path = os.path.join(config.CQ_SOURCE_PATH, 'images', f'{role_name}动画')
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)
            role_url = "https://wiki.biligame.com" + target['href']
            soup1 = self.get_soup_by_net(role_url)
            gifs = soup1.select('.floatnone>.image img')
            for gif in gifs:
                count = 1
                response = requests.get(url=gif['src'])
                file_name = str(count) + gif['alt']
                file_path = os.path.join(dir_path, file_name)
                count += 1
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
        name_storage = {'role_name': name}
        with open('./roles.json', 'w') as f:
            json.dump(name_storage, f)
        return name

    def get_role_skills(self, role_name: str) -> list:
        url = f'https://wiki.biligame.com/pcr/{role_name}#角色技能'
        response = requests.get(url=url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        skills = []
        for result in soup.find(attrs={'title': '角色技能'}).select('.wikitable'):
            try:
                tls = result.find_all('th', attrs={'style': 'text-align:left'})
                if len(tls) > 1:
                    title = tls[0].text
                    sub_title = tls[1].text
                else:
                    title = '角色达到5星后，EX技能会升级'
                    sub_title = tls[0].text
            except:
                title=''
                sub_title=''
            try:
                sls = result.find_all('td', attrs={'style': 'text-align:left'})
                skill = ''
                for s in sls:
                    skill += s.text + '\n'
            except:
                skill = ''
            try:
                image_url = result.find('img')['src']
            except:
                image_url = ''
            sdic = {
                'title': title,
                'sub_title': sub_title,
                'skill': skill,
                'image_url': image_url
            }
            skills.append(sdic)
        return skills


if __name__ == '__main__':
    w = Wiki()
    print(w.get_role_skills('真步'))
