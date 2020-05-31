from data.json.json_editor import JSONEditor
import nonebot
import config


async def alert_new_record(new_records: list, did_kill: bool):
    if len(new_records) == 0:
        return
    message = '添加了新的记录喵\n'
    for record in new_records:
        message += '- ' + record[0] + '对' + record[1] + '造成了 ' + str(record[2]) + ' 点伤害\n'
    remaining_health = JSONEditor().get_remaining_health()
    if did_kill:
        message += 'BOSS被击破了喵！干得漂亮喵！(≧▽≦)'
    else:
        message + boss_status_text(remaining_health)

    print(message)
    await nonebot.get_bot().send_group_msg(group_id=config.GROUP_ID, message=message)


def boss_status_text(remaining_health):
    message = 'BOSS血量还剩' + str(remaining_health) + '，'
    if remaining_health > 1000000:
        message += '请放心出击喵！(ฅ´ω`ฅ)'
    elif remaining_health > 600000:
        message += '请谨慎出击喵！'
    else:
        message += '可以合刀了喵！'
    return message
