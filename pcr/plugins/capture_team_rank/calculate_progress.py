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
            # TODO: 写成 = 0 if self.epoch == 1 else 1 可读性会高一些？
            now_rate = 0 if self.epoch == 1 else 1
            # 先按一个boss计算
            self.current_score += self.boss_hp[self.boss - 1] * self.score_rate[now_rate][self.boss - 1]
            if score <= self.current_score:
                # 说明加多了
                self.current_score -= self.boss_hp[self.boss - 1] * self.score_rate[now_rate][self.boss - 1]
                damage_health = (score - self.current_score) / self.score_rate[now_rate][self.boss - 1]
                # TODO: 注意此处将 damage 从 int 转为了 float。Make sure this is expected.
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
