from datetime import datetime
import os
import shutil
from distutils.dir_util import copy_tree
import sys
sys.path.insert(0,'C:\\Users\\Andrew\\Code Projects\\sftp_pi\\sftp_pi')
from sftp_pi.connection import Connection


source = r'H:\Unity Projects\Combo Enchantment Dungeon Crawler'
local_path_2 = r'C:\Users\Andrew\Code Projects\Intrepid_Descent'
remote_dir = 'IntrepidDescent'

def local_backup():
    exceptions = ''
    log = open(r'C:\Users\awest\Desktop\Unity Backup Error log.txt', 'a')
    log.write(f'\nBeginning backup {datetime.now()}\n')
    local_destination = r'C:\Users\awest\Unity Backups\Dungeon Crawler'
    for obj in os.listdir(source):
        if obj == '.git' or obj == '.vs':
            continue
        path = fr'{source}\{obj}'
        print(path)
        try:
            if os.path.isdir(path):
                copy_tree(path, fr'{local_destination}\{obj}')
            else:
                shutil.copy(path, local_destination)
        except Exception as e:
            exceptions += f'Error with {path}: {e}\n'

    log.write(exceptions)

def remote_backup():
    c = Connection('config.json', 'hostkey.ppk', 'private_key.ppk')
    dir_exclusions = ['.git', '.vs', 'Logs', 'Temp', 'Artifacts']
    file_suffix_exclusions = ['lock']
    c.upload_dir(source, remote_dir, dir_exclusions=dir_exclusions,
                 file_suffix_exclusions=file_suffix_exclusions)

def download_backup():
    c = Connection('config.json', 'hostkey.ppk', 'private_key.ppk')
    c.download(remote_dir, local_path_2)


# local_backup()
# remote_backup()
download_backup()

