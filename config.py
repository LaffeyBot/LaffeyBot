from nonebot.default_config import *

SUPERUSERS = {353884697}  # 管理员账号
COMMAND_START = {'', '/', '!', '／', '！'}  # 可作为命令起始符的字符，‘’代表没有也可以
GROUP_ID = 967350580  # 会战群
BOSS_HEALTH = [6000000, 8000000, 10000000, 12000000, 20000000]  # BOSS的血量
NAME_FOR_BOSS = ['野性狮鹫', '野性狮鹫', '野性狮鹫', '野性狮鹫', '野性狮鹫']  # BOSS的名字
MINIMUM_ATTACK = 1  # TODO
FETCH_INTERVAL = 60  # 抓取初级记录的时间（秒）
BACKUP_INTERVAL = 10  # 备份数据库的时间（分）
BACKUP_ENABLED = True  # 是否启用数据库备份
MY_NAME = '威严满满的Laffey酱'  # Bot名字
SHORT_NAME = 'Laffey酱'
SELF_INTRODUCTION = '各位指挥官好，这里是%s喵~\n' \
                    '%s会通过公会战详情界面自动记录出刀，所以各位指挥官不用手动报刀的喵！记录出击的任务就放心交给%s吧喵~\n' \
                    '目前支持的指令：\n' \
                    '【状态】可以查看当前boss的状态喵~\n' \
                    '【出刀 N】可以手动报刀N点伤害喵~\n' \
                    '【排名】可以确认公会内排名喵~\n' \
                    '【挂树】【下树】可以一键挂树/下树喵~\n' \
                    '如果指挥官忘了某项命令，可以随时通过【自我介绍】命令查看喵！\n' \
                    '还请多多关照喵~' % (MY_NAME, SHORT_NAME, SHORT_NAME)  # 自我介绍
