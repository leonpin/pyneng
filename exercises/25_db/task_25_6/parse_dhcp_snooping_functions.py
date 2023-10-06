import sqlite3
import os
from datetime import datetime, timedelta
import yaml
import re
from tabulate import tabulate

def create_db(name, schema):
    db_exists = os.path.exists(name)
    if db_exists:
        print('База данных существует')
    else:
        print('Создаю базу данных...')
        con = sqlite3.connect(name)
        with open(schema) as f:
            con.executescript(f.read())
        con.close()
    return

def add_data_switches(db_file, filename):
    db_exists = os.path.exists(db_file)
    if db_exists:
        con = sqlite3.connect(db_file)
        for file in filename:
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

def add_data(db_file, filename):
    db_exists = os.path.exists(db_file)
    if db_exists:
        con = sqlite3.connect(db_file)
        dhcp_snooping = []
        for file in filename:
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

def get_data(db_file, key, value):
    con = sqlite3.connect(db_file)
    keys = ['mac', 'ip', 'vlan', 'interface', 'switch']
    if not key in keys:
        print('Данный параметр не поддерживается.')
        print('Допустимые значения параметров:', ', '.join(keys))
        return
    #print('Информация об устройствах с такими параметрами:', key, value)
    query1 = f'select * from dhcp where {key} = ? and active=1'
    query2 = f'select * from dhcp where {key} = ? and active=0'
    try:
        with con:
            result1 = con.execute(query1, (value, ))
            result2 = con.execute(query2, (value, ))
    except sqlite3.IntegrityError as e:
        print(f'Ошибка {e}')
    result1 = result1.fetchall()
    if result1:
        print('Активные записи:')
        print(tabulate(result1))
    result2 = result2.fetchall()
    if result2:
        print('Неактивные записи:')
        print(tabulate(result2))
    con.close()
    return

def get_all_data(db_file):
    con = sqlite3.connect(db_file)
    query1 = 'select * from dhcp where active=1'
    query2 = 'select * from dhcp where active=0'
    try:
        with con:
            result1 = con.execute(query1)
            result2 = con.execute(query2)
    except sqlite3.IntegrityError as e:
        print(f'Ошибка {e}')
    #print('В таблице dhcp такие записи:')
    result1 = result1.fetchall()
    if result1:
        print('Активные записи:')
        print(tabulate(result1))
    result2 = result2.fetchall()
    if result2:
        print('Неактивные записи:')
        print(tabulate(result2))
    con.close()
    return
