import sqlite3
import sys
from tabulate import tabulate

def get_data(db_file, args):
    if len(args) == 0:
        con = sqlite3.connect(db_file)
        query = 'select * from dhcp'
        try:
            with con:
                result = con.execute(query)
        except sqlite3.IntegrityError as e:
            print(f'Ошибка {e}')
        print('В таблице dhcp такие записи:')

    elif len(args) == 2:
        con = sqlite3.connect(db_file)
        key, value = sys.argv[1:]
        keys = ['mac', 'ip', 'vlan', 'interface', 'switch']
        if not key in keys:
            print('Данный параметр не поддерживается.')
            print('Допустимые значения параметров:', ', '.join(keys))
            return
        print('Информация об устройствах с такими параметрами:', key, value)
        query = f'select * from dhcp where {key} = ?'
        try:
            with con:
                result = con.execute(query, (value, ))
        except sqlite3.IntegrityError as e:
            print(f'Ошибка {e}')
    else:
        print('Пожалуйста, введите два или ноль аргументов')
        return
    print(tabulate(result))
    con.close()
    return



if __name__ == "__main__":
    db_file = 'dhcp_snooping.db'
    args = sys.argv[1:]
    get_data(db_file, args)