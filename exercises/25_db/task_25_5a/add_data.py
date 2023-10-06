import sqlite3
import os
import re
import yaml
import glob
from datetime import datetime, timedelta

def add_switches(db_name, file):
    db_exists = os.path.exists(db_name)
    if db_exists:
        con = sqlite3.connect(db_name)
        with open(file) as f:
            switches = yaml.safe_load(f)
        print('Добавляю данные в таблицу switches...')
        for key, value in switches['switches'].items():
            query = 'insert into switches values (?, ?)'
            try:
                with con:
                    con.execute(query, (key, value))
            except sqlite3.IntegrityError as e:
                print(f'При добавлении данных:{(key, value)} Возникла ошибка:{e}')
        con.close()
    else:
        print('База данных не существует. Перед добавлением данных ее надо создать')
    return

def add_dhcp(db_name, files):
    db_exists = os.path.exists(db_name)
    if db_exists:
        con = sqlite3.connect(db_name)
        dhcp_snooping = []
        for file in files:
            with open(file) as f:
                for line in f:
                    match = re.search(r'(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)', line)
                    if match:
                        sw = re.search(r'(\w+)_dhcp_snooping.txt', file).group(1)
                        dhcp_snooping.append([*match.groups(), sw])
        print('Добавляю данные в таблицу dhcp...')
        query = 'update dhcp set active=0'
        con.execute(query)
        week_ago = datetime.today().replace(microsecond=0) - timedelta(days=7)
        query = 'delete from dhcp where last_active < ?'
        con.execute(query, (week_ago, ))
        for row in dhcp_snooping:
            query = 'replace into dhcp values (?, ?, ?, ?, ?, 1, datetime("now"))'
            try:
                with con:
                    con.execute(query, row)
            except sqlite3.IntegrityError as e:
                print(f'При добавлении данных:{row} Возникла ошибка:{e}')
        con.close()
    else:
        print('База данных не существует. Перед добавлением данных ее надо создать')
    return

if __name__ == "__main__":
    db_name = 'dhcp_snooping.db'
    #dhcp_files = glob.glob('sw*_dhcp_snooping.txt')
    dhcp_files = glob.glob('new_data/sw*_dhcp_snooping.txt')
    switches_file = 'switches.yml'
    add_dhcp(db_name, dhcp_files)
    add_switches(db_name, switches_file)