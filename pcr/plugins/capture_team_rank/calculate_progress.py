import config


class Progress(object):
    def __init__(self):
        self.boss_hp = config.BOSS_HEALTH
        self.score_rate = [
            [1, 1, 1.1, 1.1, 1.2],
            [1.2, 1.2, 1.5, 1.7, 2],
        ]
        self.epoch = 1
        self.damage = 0
        self.boss = 1
        self.current_score = 0

    def get_result(self, score: int = 0) -> str:
        while True:
            now_rate = 2 - 1 if self.epoch > 2 else self.epoch - 1
            # 先按一个boss计算
            self.current_score += self.boss_hp[self.boss - 1] * self.score_rate[now_rate][self.boss - 1]
            if score <= self.current_score:
                # 说明加多了
                self.current_score -= self.boss_hp[self.boss - 1] * self.score_rate[now_rate][self.boss - 1]
                damage_health = (score - self.current_score) / self.score_rate[now_rate][self.boss - 1]
                self.damage += damage_health
                remain_health = self.boss_hp[self.boss - 1] - damage_health
                remain_percent = round((1 - damage_health / self.boss_hp[self.boss - 1]) * 100, 2)
                print(remain_percent)
                break
            if self.boss + 1 > 5:
                self.boss = 1
                self.epoch += 1
            else:
                self.boss += 1
        return f'当前该公会正在攻略{self.epoch}周目第{self.boss}王：\n' \
               f'{int(remain_health)}/{self.boss_hp[self.boss-1]},剩余血量占比{remain_percent}%\n'


if __name__ == '__main__':
    p = Progress()
    print(p.get_result(800577184))
