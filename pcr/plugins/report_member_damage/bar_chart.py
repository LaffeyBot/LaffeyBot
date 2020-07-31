import matplotlib.pyplot as plt
import numpy as np


class MemberDamageChart(object):
    def __init__(self, title_name: str, player_name: list, damage: list, file_path: str):
        plt.rcParams["font.family"] = "SimHei"
        # 初始画布
        self.fig = plt.figure(num=f'{title_name}', figsize=(8, 6))
        self.ax = self.fig.add_subplot(111)
        # 初始化参数
        self.title_name = title_name
        self.player_name = player_name
        self.damage = damage
        self.file_path = file_path

    def sort_damage(self) -> dict:
        # 返回一个tuple的list,如[(2333,'xxx')],顺序是伤害逆序
        return dict(sorted(list(zip(self.damage, self.player_name))))

    def make_chart(self):
        damage_max = max(self.damage)
        damage_min = min(self.damage)
        member_num = len(self.player_name)
        sorted_name = [i for i in self.sort_damage().values()]
        sorted_damage = sorted(self.damage, reverse=True)
        color_list = ['cyan'] * member_num
        self.ax.set_xlim([0.5, member_num + 0.5])
        print(self.player_name)
        print(np.arange(1, member_num, member_num), sorted_damage)
        if damage_min - 200 <= 0:
            self.ax.set_ylim([0, damage_max + 200])
        else:
            self.ax.set_ylim([damage_min - 200, damage_max + 200])
        self.ax.set_ylabel('玩家伤害', fontsize=18)
        self.ax.bar(x=np.arange(1, member_num + 1), height=sorted_damage,
                    color=color_list \
                    , bottom=0.5, linewidth=1, width=0.6, alpha=1)
        # 设置显示刻度
        self.ax.set_xticks(np.linspace(1, member_num, member_num))
        gap = (damage_max - damage_min + 400) // 500 + 1
        if gap <= 12:
            self.ax.set_yticks(np.linspace(damage_max + 200, damage_min - 200, gap))
        else:
            self.ax.set_yticks(np.linspace(damage_max + 200, damage_min - 200, 12))

        self.ax.set_xticklabels(sorted_name, fontproperties="SimHei" \
                                , fontsize=12)
        for x, y in zip(np.linspace(1, member_num, member_num), sorted_damage):
            if y < 10000:
                self.ax.text(x - 0.3, y + 2, f'{y}', fontsize=12)
            else:
                self.ax.text(x - 0.3, y + 4, f'{y/10000}w', fontsize=12)
        self.ax.spines["top"].set_visible(False)  # 上轴不显示
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_visible(False)
        self.ax.spines["bottom"].set_linewidth(3)
        self.ax.tick_params(pad=4, left=False)
        self.ax.set_title(f"{self.title_name}", fontsize=18, backgroundcolor='yellowgreen', \
                          fontweight='bold', color='white')

        self.ax.yaxis.grid(linewidth=0.5, color="black", alpha=0.5)
        self.ax.set_axisbelow(True)  # 网格显现在图形下方

    def get_chart(self):
        self.make_chart()
        # 这句代码必须加上，不然无法显示全图
        plt.tight_layout()
        plt.savefig(self.file_path, dpi=100)
        plt.close()


if __name__ == '__main__':
    nl = [str(i) + "哈哈" for i in range(10)]
    dl = [i for i in range(1000, 2000, 100)]
    m = MemberDamageChart('xx月成员伤害统计', nl, dl, './demo.jpg')
    m.get_chart()
