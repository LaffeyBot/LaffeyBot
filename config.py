from nonebot.default_config import *

HOST = '127.0.0.1'
PORT = 8081
SUPERUSERS = {353884697}  # 管理员账号
COMMAND_START = {'', '/', '!', '／', '！'}  # 可作为命令起始符的字符，‘’代表没有也可以
#GROUP_ID = 967350580  # 会战群
#GROUP_ID = 1108319335
GROUP_ID = 826407504
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
                  f'最后，{SHORT_NAME}希望指挥官能跟其他指挥官多商量一下公会战的策略喵~\n' \
                  f'还请多多关照喵~'     # 新增群成员欢迎信息
SENDER_ADDRESS = "3461372627@qq.com"   # 反馈发送服务器
SENDER_PWD = "uxoximotyatnciii"   # 邮箱授权码
#RECEIVE_ADDRESS = "3551318424@qq.com"   # 开发者邮箱地址
RECEIVE_ADDRESS = "zjdavid.2003@gmail.com"
LAFFEY_MESSAGE = ['本森级驱逐舰拉菲听候您的吩咐……指挥官，这个耳朵不是真的，请不要再盯着看了……',
                    '指挥官休息的还好吗，拉菲现在很有精神，大概',
                    '指挥官不理拉菲，哈啊……都要睡着噜……',
                    '嗯？这是拉菲心情好的表现喔',
                    '指挥官指挥官，拉菲，可，怕，吗？',
                    '指挥官……莫非是变态？！',
                    '一开始，感觉指挥官有点无聊……不过仔细想想，我除了战斗也很没干劲，说不定我和指挥官很合得来喔……',
                    '虽然过去习惯一个人了……和指挥官一起的话，总觉得这样更好……呣……呼……Zzzzzz……',
                    '原本还一直想着，为了指挥官的话，就算再次化身鬼神也无所谓…不过…被指挥官这么关心着…看来是没有机会了呢…指挥官…失望吗？',
                    '标枪，绫波，Z23……都是好朋友，想和她们，还有大家一直在一起 ',
                  '指挥官…无论拉菲变成怎么样都喜欢拉菲…？虽然不太明白，那应该就是指挥官会一直陪着拉菲的意思吧',
                  '就算指挥官盯着别人看，拉菲也不会生气的。嗯，真的，一，点，都，不，生，气，的。',
                  '就算指挥官再怎么照顾拉菲，拉菲也不会过度依赖指挥官的。嗯，不会变成习惯被饲养的废柴的',
                  '无论遇到什么困难，拉菲都一定会回到指挥官身边的。因为，拉菲这样和指挥官约好了的',
                  '拉菲得了离开指挥官就没有精神的病。拉菲没有说谎，是真的。',
                  '拉菲，快要适应指挥官这些奇怪的想法了',
                  '因为睡觉被z23说教了…z23好严格…',
                  '绫波，好像很努力的样子，拉菲不能输。但是拉菲有些困了，怎么办……',
                  '拉菲，快要适应指挥官这些奇怪的想法了']   # Laffey定时问候语，TODO 爬虫添加
