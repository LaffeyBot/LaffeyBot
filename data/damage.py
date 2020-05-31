from data.init import get_connection
import time


def add_record(records: list) -> list:
    # 传入一个list，将list数据与已有数据比对，如果不同则添加进去
    # 最后传回新添加的数据（以list形式）
    # Example List: [['User1', '野性狮鹫', '183197'], ['User2', '野性狮鹫', '27891']...]
    today = int(time.strftime("%Y%m%d", time.localtime()))
    print(today)
    c = get_connection()
    today_records = c.execute('SELECT username, target, damage'
                              ' FROM record WHERE date=?', (today,)).fetchall()
    added_records = list()
    record: list
    for record in records:
        if next(filter(lambda r: r[0] == record[0] and r[2] == record[2], today_records), None) is not None:
            continue  # Record 已存在
        added_records.append(record)
        record.append(today)
        c.execute("INSERT INTO record (username, target, damage, date) VALUES "
                  "(?, ?, ?, ?)", record)
    c.commit()
    return added_records


class RecordDamage:

    def get_record(self, date) -> list:
        # TODO: 根据参数（date...）返回符合要求的记录
        return list()

    def delete_record(self, object_id):
        # TODO: 根据参数（date/id...）删除符合要求的记录
        pass
