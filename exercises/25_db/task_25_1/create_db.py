import os
import sqlite3

def create_db(db_name, schema_file):
    db_exists = os.path.exists(db_name)
    if db_exists:
        print('База данных существует')
    else:
        print('Создаю базу данных...')
        con = sqlite3.connect(db_name)
        with open(schema_file) as f:
            con.executescript(f.read())
        con.close()
    return

if __name__ == "__main__":
    db_name = 'dhcp_snooping.db'
    schema_file = 'dhcp_snooping_schema.sql'
    create_db(db_name, schema_file)