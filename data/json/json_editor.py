import json
from config import BOSS_HEALTH


class JSONEditor:
    def __init__(self):
        with open('status.json', 'r') as file:
            self.dict = json.load(file)

    def save(self):
        with open('status.json', 'w') as file:
            json.dump(self.dict, file)

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

    def kill_boss(self):
        if self.dict['current_boss_order'] != 5:
            self.dict['current_boss_order'] += 1
        else:
            self.dict['current_boss_order'] = 1
            self.dict['current_generation'] += 1

        current_order = self.dict['current_boss_order']
        self.set_remaining_health(BOSS_HEALTH[current_order-1])  # 将血量设置到下一个boss
