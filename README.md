# PCRBot
   一个PCR（公主连结）的公会战辅助机器人，具有自动记录，汇报伤害的功能。
   
# 自动流程

1. [scheduler.py](https://github.com/zjdavid/PCRBot/blob/master/pcr/plugins/scheduler.py) 将会周期性（默认30秒）读取截屏文件夹，并将截屏文件交给[ocr.py](https://github.com/zjdavid/PCRBot/blob/master/pcr/plugins/ocr.py) 处理
2. [ocr.py](https://github.com/zjdavid/PCRBot/blob/master/pcr/plugins/ocr.py) 会尝试识别出图片中的出刀记录并传回。
3. [scheduler.py](https://github.com/zjdavid/PCRBot/blob/master/pcr/plugins/scheduler.py) 会将数据传给 [damage_record.py](https://github.com/zjdavid/PCRBot/blob/master/pcr/plugins/damage_record.py)
4. [record_damage.py](https://github.com/zjdavid/PCRBot/blob/master/pcr/plugins/damage_record.py) 会记录下此次伤害记录
5. 随后，[scheduler.py](https://github.com/zjdavid/PCRBot/blob/master/pcr/plugins/scheduler.py) 会调用 QQ 机器人汇报新增出刀。

# QQ 机器人功能


- 出刀 n：手动出刀，对当前boss造成n点伤害
- 挂树：一键挂树。将会在当前boss被击破时自动通知并取消挂树
- TODO: 出刀提醒：会在指定时间提醒x人已经出刀了。在 config.py 中可以设定以下内容：
    - MINIMUM_ATTACKS：每天的最低出刀数。如果为零则关闭提醒。提醒数量会包括所有出刀数到达x的玩家。
    - ATTACK_NOTIFICATION_TIME：提醒时间
- 今日出刀：TODO返回今日出刀记录汇总
- 修正: TODO 手动纠正不正确的识别
。。。

# Quick Start Guide
本项目依赖以下第三方软件
- [Tesseract](https://tesseract-ocr.github.io/tessdoc/Home.html)
- [Android Debug Bridge](https://developer.android.com/studio/releases/platform-tools)
- 安卓模拟器（本程序仅在网易Mumu上测试过）
- 酷Q + [cqhttp](https://github.com/richardchien/coolq-http-api)
