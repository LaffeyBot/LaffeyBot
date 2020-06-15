import os
from data.init_database import get_connection


def update_picture_list():
    c = get_connection()

    # noinspection SqlWithoutWhere
    c.execute('DELETE FROM picture_list')
    for file_name in os.listdir('pictures/untagged/'):
        c.execute('INSERT INTO picture_list (file_name, sub_directory, origin)  '
                  'VALUES (?, ?, ?)', (file_name, 'untagged', ''))

    for file_name in os.listdir('pictures/tagged/'):
        pixiv_id = file_name.split('_')[0]
        origin = 'https://www.pixiv.net/artworks/' + pixiv_id
        c.execute('INSERT INTO picture_list (file_name, sub_directory, origin)  '
                  'VALUES (?, ?, ?)', (file_name, 'tagged', origin))

    c.commit()

