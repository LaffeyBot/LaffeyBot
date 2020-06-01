import os
import shutil
from datetime import datetime


def backup():
    if not os.path.isdir('backup'):
        os.mkdir('backup')

    if os.path.isfile('main.db'):
        current_time = datetime.now().strftime("%Y-%m-%d-%H-%M")
        backup_file_name = 'backup/main-' + current_time + '.db'
        shutil.copy2('main.db', backup_file_name)
