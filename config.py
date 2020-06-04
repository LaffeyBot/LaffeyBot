from nonebot.default_config import *

HOST = '127.0.0.1'
PORT = 8083
SUPERUSERS = {353884697}  # 管理员账号
COMMAND_START = {'', '/', '!', '／', '！'}  # 可作为命令起始符的字符，‘’代表没有也可以
GROUP_ID = 967350580  # 会战群
# GROUP_ID = 1108319335
BOSS_HEALTH = [6000000, 8000000, 10000000, 12000000, 20000000]  # BOSS的血量
NAME_FOR_BOSS = ['双足飞龙', '野性狮鹫', '兽人头目', '灵魂角鹿', '弥诺陶洛斯']  # BOSS的名字
MINIMUM_ATTACK = 1  # TODO
FETCH_INTERVAL = 120  # 抓取初级记录的时间（秒）
BACKUP_INTERVAL = 10  # 备份数据库的时间（分）
BACKUP_ENABLED = True  # 是否启用数据库备份
MY_NAME = '威严满满的Laffey酱'  # Bot名字
SHORT_NAME = 'Laffey酱'
DO_REFRESH_DATA = True
SELF_INTRODUCTION = '各位指挥官好，这里是%s喵~\n' \
                    '%s会通过公会战详情界面自动记录出刀，所以各位指挥官不用手动报刀的喵！记录出击的任务就放心交给%s吧喵~\n' \
                    '目前支持的指令：\n' \
                    '【状态】可以查看当前boss的状态喵~\n' \
                    '【出刀 N】可以手动报刀N点伤害喵~\n' \
                    '【排名】可以确认公会内排名喵~\n' \
                    '【挂树】【下树】可以一键挂树/下树喵~\n' \
                    '【停止汇报】【开始汇报】可以关闭/开启【发送者】的出刀汇报\n' \
                    '【出刀报告】可以查看今日出刀次数的汇总报告\n' \
                    '【出刀详情】可以查看每位玩家的出刀次数\n' \
                    '如果指挥官忘了某项命令，可以随时通过【自我介绍】命令查看喵！\n' \
                    '还请多多关照喵~' % (MY_NAME, SHORT_NAME, SHORT_NAME)  # 自我介绍
WELCOME_MESSAGE = f'这里是{MY_NAME}为指挥官提供服务喵~\n' \
                  f'{SHORT_NAME}的职责就是监督指挥官完成好每天公会战三次出击情况的喵~\n' \
                  f'因此，指挥官在这里想摸鱼是不可以的喵~\n' \
                  f'指挥官可以通过【自我介绍】命令查看{SHORT_NAME}的功能喵~\n' \
                  f'希望指挥官能够和司令部的其他指挥官在这里玩的开心喵~\n' \
                  f'最后，{SHORT_NAME}希望指挥官能跟其他指挥官多商量一下公会战的策略喵~' \
                  f'还请多多关照喵~'
