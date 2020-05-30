# PCRBot
   一个PCR（公主连结）的公会战辅助机器人，具有自动记录，汇报伤害的功能。
   
# 自动流程

1. scheduler.py将会周期性（默认30秒）读取截屏文件夹，并将截屏文件交给[ocr.py](https://github.com/zjdavid/PCRBot/blob/master/pcr/plugins/ocr.py)处理
2. [ocr.py](https://github.com/zjdavid/PCRBot/blob/master/pcr/plugins/ocr.py)会尝试识别出图片中的出刀记录并传回record_bot.py。
- 注意：中文识别不可靠，可能需要模糊匹配
3. scheduler.py 会将数据传给 record_damage.py
4. record_damage.py 会记录下此次伤害记录并调用QQ 机器人汇报新增出刀。

# QQ 机器人功能

- 今日出刀：返回今日出刀记录汇总
- 挂树：一键挂树  // TODO: 将会在当前boss被击破时自动通知并取消挂树
- 修正: 手动纠正不正确的识别
。。。

# Quick Start Guide
TODO
