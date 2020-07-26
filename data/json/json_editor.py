import json
from config import BOSS_HEALTH
from aiocqhttp.event import Event
import os


class JSONEditor:
    def __init__(self, group_id: int):
        if not os.path.isdir('status'):
            os.mkdir('status')
        file_name = 'status/status_' + str(group_id) + '.json'
        if not os.path.isfile(file_name):
            self.init_json_for_group(file_name)
        self.load_json(file_name)

    def load_json(self, file_name):
        with open(file_name, 'r') as file:
            try:
                self.dict: dict = json.load(file)
            except:
                self.init_json_for_group(file_name)
                self.load_json()

    @staticmethod
    def init_json_for_group(path):
        init_dict: dict = {"current_generation": 1,
                           "current_boss_order": 1,
                           "remaining_health": 600000,
                           "tree": [], "fetch_status": True,
                           "no_report": []}
        with open(path, 'w+') as file:
            json.dump(init_dict, file)

    def save(self):
        with open('status.json', 'w') as file:
            json.dump(self.dict, file)

    def get_fetch_status(self) -> bool:
        return self.dict.get('fetch_status', True)

    def set_fetch_status(self, status: bool):
        self.dict['fetch_status'] = status
        self.save()

    def get_remaining_health(self):
        return self.dict['remaining_health']

    def set_remaining_health(self, health: int):
        self.dict['remaining_health'] = health
        self.save()

    def get_current_boss_order(self) -> int:
        return self.dict['current_boss_order']

    def get_generation(self) -> int:
        return self.dict['current_generation']

    def add_damage(self, damage: int) -> bool:
        remaining_health: int = self.get_remaining_health()
        print('ADD_DAMAGE ' + str(damage))
        print('REMAINING ' + str(remaining_health))
        did_kill_boss = False
        if damage >= remaining_health:
            # 击破
            self.kill_boss()
            did_kill_boss = True
        else:
            self.set_remaining_health(remaining_health - damage)
        self.save()
        return did_kill_boss

    def add_on_tree(self, name):
        if self.dict.get('tree', None) is None:
            self.dict['tree'] = [name]
        elif name in self.dict['tree']:
            tree: list = self.dict['tree']
            tree.append(name)
            self.dict['tree'] = tree
        self.save()

    def remove_from_tree(self, name):
        if self.dict.get('tree', None) is not None:
            tree: list = self.dict['tree']
            if name in tree:
                tree.remove(name)
                self.dict['tree'] = tree
                self.save()

    def add_to_no_report_list(self, name):
        if self.dict.get('no_report', None) is None:
            self.dict['no_report'] = [name]
        else:
            no_report: list = self.dict['no_report']
            no_report.append(name)
            self.dict['no_report'] = no_report
        self.save()

    def remove_from_no_report_list(self, name):
        if self.dict.get('no_report', None) is not None:
            no_report: list = self.dict['no_report']
            if name in no_report:
                no_report.remove(name)
                self.dict['no_report'] = no_report
            self.save()

    def get_no_report_list(self):
        return self.dict.get('no_report', list())

    def clear_tree(self) -> list:
        tree: list = self.dict['tree']
        self.dict['tree'] = list()
        self.save()
        return tree

    def exists_player_on_tree(self) -> bool:
        if self.dict.get('tree', None) is None:
            return False
        return len(self.dict['tree']) > 0

    def kill_boss(self):
        if self.dict['current_boss_order'] != 5:
            self.dict['current_boss_order'] += 1
        else:
            self.dict['current_boss_order'] = 1
            self.dict['current_generation'] += 1

        current_order = self.dict['current_boss_order']
        self.set_remaining_health(BOSS_HEALTH[current_order - 1])  # 将血量设置到下一个boss

    def do_repeat(self, cq_event: Event) -> bool:
        do_repeat = False
        if 'message' in self.dict and self.dict['message'] == dict(cq_event.message[0]):
            self.dict['message_count'] += 1
            self.dict['message_users'].append(cq_event.sender['user_id'])
            # print()
            if self.dict['message_count'] >= 3 and len(set(self.dict['message_users'])) > 1:
                self.dict['message_count'] = 0
                self.dict['message_users'] = []
                self.dict['message'] = dict()
                do_repeat = True
        else:
            self.dict['message'] = cq_event.message[0]
            self.dict['message_count'] = 1
            self.dict['message_users'] = [cq_event.sender['user_id']]
        self.save()
        return do_repeat
