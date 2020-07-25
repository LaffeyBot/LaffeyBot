from data.init_database import get_connection
import config


class PictureQuota:
    def __init__(self, qq_id=0):
        self.qq_id = qq_id
        self.c = get_connection()

    def get_one_picture(self) -> bool:
        cursor = self.c.cursor()
        existing_data_record = cursor.execute('SELECT * '
                                              'FROM picture_quota'
                                              ' WHERE qq_id=%s', (self.qq_id,))
        existing_data: (str, int) = cursor.fetchone()
        print(existing_data_record)
        if existing_data_record == 0:
            cursor.execute('INSERT INTO picture_quota (qq_id, count) '
                           'VALUES (%s, %s)', (self.qq_id, 1))
        else:
            original_count = existing_data[1]
            if original_count >= config.PICTURE_QUOTA:
                return False
            original_count += 1
            cursor.execute('UPDATE picture_quota SET count=%s WHERE qq_id=%s'
                           , (original_count, self.qq_id))

        self.c.commit()
        return True

    def clear_quota(self):
        # noinspection SqlWithoutWhere
        self.c.cursor().execute('DELETE FROM picture_quota')
        self.c.commit()
