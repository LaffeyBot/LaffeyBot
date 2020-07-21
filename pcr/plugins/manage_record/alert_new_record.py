from data.json.json_editor import JSONEditor
import nonebot
import config


async def alert_new_record(new_records: list, did_kill: bool):
    if len(new_records) == 0:
        return
    message = '添加了新的记录喵\n'

    no_report_list = JSONEditor().get_no_report_list()
    for record in new_records:
        if record[0] in no_report_list:
            new_records.remove(record)
    if len(new_records) == 0:
        return  # 不汇报

    for record in new_records:
        message += '- ' + record[0] + '对' + record[1] + '造成了 ' + str(record[2]) + ' 点伤害\n'
    remaining_health = JSONEditor().get_remaining_health()
    if did_kill:
        message += 'BOSS被击破了喵！干得漂亮喵！(≧▽≦)'
        if JSONEditor().exists_player_on_tree():
            message += '\n'
            for player in JSONEditor().clear_tree():
                message += '@' + player + ' '
            message += '可以从树上下来了喵~'
    else:
        message += boss_status_text(remaining_health)

    print(message)
    await nonebot.get_bot().send_group_msg(group_id=config.PRIMARY_GROUP_ID, message=message)


def boss_status_text(remaining_health):
    message = 'BOSS血量还剩' + str(remaining_health) + '，'
    if remaining_health > 1000000:
        message += '请放心出击喵！(ฅ´ω`ฅ)'
    elif remaining_health > 600000:
        message += '请谨慎出击喵！'
    else:
        message += '可以合刀了喵！'
    return message
