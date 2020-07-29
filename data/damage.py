from data.init_database import get_connection
from data.json.json_editor import JSONEditor
from data.player_name import get_closest_player_name
from data.get_date_int import get_date_int
from datetime import datetime
import config


def add_record(records: list, group_id: int, force=False) -> (list, bool):
    # 传入一个list，将list数据与已有数据比对，如果不同则添加进去
    # 最后传回新添加的数据（以list形式）
    # Example List: [['User1', '野性狮鹫', '183197'], ['User2', '野性狮鹫', '27891']...]
    today = get_date_int(datetime.now())
    print(today)
    c = get_connection()
    cursor = c.cursor()
    json_editor = JSONEditor(group_id)

    added_records = list()
    killed_boss = False
    record: list
    for record in reversed(records):
        # 修正target和用户名
        record[1] = config.NAME_FOR_BOSS[json_editor.get_current_boss_order() - 1]
        record[0] = get_closest_player_name(record[0], group_id)

        existing_count = cursor.execute('SELECT * FROM record '
                                        'WHERE damage=%s AND group_id = %s',
                                        (record[2], group_id))
        if not force and existing_count > 0:
            continue  # 如果不是强制记录并且 Record 已存在
        record.append(today)
        record.append(group_id)

        remaining_health = json_editor.get_remaining_health()
        did_kill = json_editor.add_damage(damage=int(record[2]))
        if did_kill:
            killed_boss = True
            record[2] = remaining_health

        cursor.execute("INSERT INTO record (username, target, damage, date, group_id) VALUES "
                       "(%s, %s, %s, %s, %s)", tuple(record))
        added_records.append(record)
        print('DAMAGE ' + str(int(record[2])))

    c.commit()
    return added_records, killed_boss


# noinspection SqlWithoutWhere
def delete_all_records(group_id: int):
    c = get_connection()
    c.execute('DELETE FROM record WHERE group_id=%s', (group_id,))
    c.commit()
