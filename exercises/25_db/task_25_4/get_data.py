import sqlite3
import sys
from tabulate import tabulate

def get_data(db_file, args):
    if len(args) == 0:
        con = sqlite3.connect(db_file)
        query1 = 'select * from dhcp where active=1'
        query2 = 'select * from dhcp where active=0'
        try:
            with con:
                result1 = con.execute(query1)
                result2 = con.execute(query2)
        except sqlite3.IntegrityError as e:
            print(f'Ошибка {e}')
        print('В таблице dhcp такие записи:')

    elif len(args) == 2:
        con = sqlite3.connect(db_file)
        key, value = args
        keys = ['mac', 'ip', 'vlan', 'interface', 'switch']
        if not key in keys:
            print('Данный параметр не поддерживается.')
            print('Допустимые значения параметров:', ', '.join(keys))
            return
        print('Информация об устройствах с такими параметрами:', key, value)
        query1 = f'select * from dhcp where {key} = ? and active=1'
        query2 = f'select * from dhcp where {key} = ? and active=0'
        try:
            with con:
                result1 = con.execute(query1, (value, ))
                result2 = con.execute(query2, (value, ))
        except sqlite3.IntegrityError as e:
            print(f'Ошибка {e}')
    else:
        print('Пожалуйста, введите два или ноль аргументов')
        return
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

if __name__ == "__main__":
    db_file = 'dhcp_snooping.db'
    args = sys.argv[1:]
    #args = ['vlan', 1]
    get_data(db_file, args)