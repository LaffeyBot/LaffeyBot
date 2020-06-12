from data.init_database import init_database, get_connection
import os
import csv
from pcr.plugins.backup import backup
from data.update_picture_list import update_picture_list


backup()  # 备份之前的数据库

init_database()

update_picture_list()

if os.path.isfile('player_list.csv'):
    with open('player_list.csv', 'r', encoding='UTF-8') as file:
        f_csv = csv.reader(file)
        headers = next(f_csv)

        c = get_connection()
        # noinspection SqlWithoutWhere
        c.execute('DELETE FROM player_list')

        if headers[0] == 'game_name':
            player_name_row = 0
            qq_name_row = 1
        else:
            player_name_row = 1
            qq_name_row = 0
        for row in f_csv:
            # print(row)
            c.execute('INSERT INTO player_list (qq_name, player_name) '
                      'VALUES (?, ?)', (row[qq_name_row], row[player_name_row]))

        c.commit()


