from data.model import Records, Groups
import config


def damage_to_score(record: Records) -> int:
    if record.boss_gen == 1:
        multiplier = [1.0, 1.0, 1.1, 1.2, 1.3]
    else:
        multiplier = [1.2, 1.3, 1.5, 1.7, 2.0]
    return int(record.damage * multiplier[record.boss_gen-1])


def subtract_damage_from_group(record: Records, group: Groups):
    if record.damage < group.boss_remaining_health:
        group.boss_remaining_health -= record.damage
    else:
        if group.current_boss_order < 5:
            group.current_boss_order += 1
        else:
            group.current_boss_order = 1
            group.current_boss_gen += 1
        group.boss_remaining_health = config.BOSS_HEALTH[group.current_boss_order-1]
