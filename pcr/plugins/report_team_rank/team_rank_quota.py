import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import time as ti


class TeamRankChart(object):
    def __init__(self, times: list, ranks: list, filepath='./demo.jpg'):
        # 初始化折线图全局操作
        self.time = times
        self.rank = ranks
        self.file_path = filepath
        # 创建画布
        self.fig = plt.figure(num='公会实时排名图', figsize=(8, 6))
        # 选择子图
        self.ax = self.fig.add_subplot(111)
        # 全局中文显示处理
        plt.rcParams['font.family'] = 'SimHei'

    def get_max_rank(self):
        return max(self.rank)

    def get_min_rank(self):
        return min(self.rank)

    def make_chart(self):
        rmin = self.get_min_rank() // 100 * 100
        rmax = self.get_max_rank() // 100 * 100
        time_length = len(self.time)
        # 设置刻度范围
        self.ax.set_xlim([0.5, time_length + 0.1])  # x轴从1到记录最长时间
        if rmin - 200 <= 0:
            self.ax.set_ylim([0, rmax + 200])
        else:
            self.ax.set_ylim([rmin - 200, rmax + 200])  # y轴从最小rank-100到最大rank+100
        # 设置显示刻度
        if time_length <= 20:
            self.ax.set_xticks(np.linspace(1, time_length, time_length))
        gap = (rmax - rmin + 400) // 500 + 1
        if gap <= 12:
            self.ax.set_yticks(np.linspace(rmax + 200, rmin - 200, gap))
        else:
            self.ax.set_yticks(np.linspace(rmax + 200, rmin - 200, 12))
        # self.ax.set_xticklabels(self.time, fontproperties="SimHei", fontsize=12, rotation=-30)
        # 设置刻度线
        self.ax.tick_params(left=True, direction="in", length=2, width=2, color='b', labelsize="medium")
        self.ax.tick_params(bottom=True, direction="in", length=2, width=2, color='b', labelsize="medium")
        # 设置标题
        self.ax.set_title(f"{datetime.now().month} 月 公 会 战 公 会 实 时 排 名", fontsize=14, backgroundcolor='#3c7f99',
                          fontweight='bold', color='white', verticalalignment="center", fontproperties="SimHei")
        # 去掉上右边框
        self.ax.spines["left"].set_color("darkblue")
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        # 添加图例
        x = np.arange(1, len(self.time) + 1)
        self.ax.plot(x, self.rank, color='#57faff', marker='.', label='当前排名')
        self.ax.legend(loc=2, handlelength=3, fontsize=14, shadow=True)
        # 添加标签
        self.ax.text(self.rank.index(self.get_max_rank()) + 1, self.get_max_rank() + 3, f"最低排名:{self.get_max_rank()}",
                     fontsize=14, color='g', alpha=0.75)
        self.ax.text(self.rank.index(self.get_min_rank()) + 1, self.get_min_rank() - 20, f"最好排名:{self.get_min_rank()}",
                     fontsize=14, color='g',
                     alpha=0.75)
        # plt.show()

    def get_chart(self):
        self.make_chart()
        # 这句代码必须加上，不然无法显示全图
        plt.tight_layout()
        plt.savefig(self.file_path, dpi=100)
        plt.close()


if __name__ == '__main__':
    time = [str(i) + '月' for i in range(1, 7)]
    rank = [10201, 9800, 8200, 12500, 6677, 6000]
    t = TeamRankChart(time, rank)
    print('1')
    t.get_chart()
    print('2')
    ti.sleep(20)
    print('=')
