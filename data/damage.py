from data.init_database import get_connection
from data.json.json_editor import JSONEditor
from data.player_name import get_closest_player_name
from data.get_date_int import get_date_int
from datetime import datetime
import config


def add_record(records: list, force=False) -> (list, bool):
    # 传入一个list，将list数据与已有数据比对，如果不同则添加进去
    # 最后传回新添加的数据（以list形式）
    # Example List: [['User1', '野性狮鹫', '183197'], ['User2', '野性狮鹫', '27891']...]
    today = get_date_int(datetime.now())
    print(today)
    c = get_connection()
    json_editor = JSONEditor()

    added_records = list()
    killed_boss = False
    record: list
    for record in reversed(records):
        # 修正target和用户名
        record[1] = config.NAME_FOR_BOSS[JSONEditor().get_current_boss_order() - 1]
        record[0] = get_closest_player_name(record[0])

        if not force and c.execute('SELECT * FROM record WHERE damage=?',
                                   (record[2],)).fetchone() is not None:
            continue  # 如果不是强制记录并且 Record 已存在
        added_records.append(record)
        record.append(today)
        c.execute("INSERT INTO record (username, target, damage, date) VALUES "
                  "(?, ?, ?, ?)", tuple(record))
        print('DAMAGE ' + str(int(record[2])))
        did_kill = json_editor.add_damage(damage=int(record[2]))
        if did_kill:
            killed_boss = True

    c.commit()
    return added_records, killed_boss


# noinspection SqlWithoutWhere
def delete_all_records():
    c = get_connection()
    c.execute('DELETE FROM record')
    c.commit()


class RecordDamage:

    def get_record(self, date) -> list:
        # TODO: 根据参数（date...）返回符合要求的记录
        return list()

    def delete_record(self, object_id):
        # TODO: 根据参数（date/id...）删除符合要求的记录
        pass
