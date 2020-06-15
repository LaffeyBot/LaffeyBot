from data.init_database import get_connection
import config


class PictureQuota:
    def __init__(self, qq_id=0):
        self.qq_id = qq_id
        self.c = get_connection()

    def get_one_picture(self) -> bool:
        existing_data = self.c.execute('SELECT qq_id, count FROM picture_quota WHERE qq_id=?', (self.qq_id,)).fetchone()
        print(existing_data)
        if existing_data is None:
            self.c.execute('INSERT INTO picture_quota (qq_id, count) '
                           'VALUES (?, ?)', (self.qq_id, 1))
        else:
            original_count = existing_data[1]
            if original_count >= config.PICTURE_QUOTA:
                return False
            original_count += 1
            self.c.execute('UPDATE picture_quota SET count=? WHERE qq_id=?'
                           , (original_count, self.qq_id))

        self.c.commit()
        return True

    def clear_quota(self):
        # noinspection SqlWithoutWhere
        self.c.execute('DELETE FROM picture_quota')
        self.c.commit()
