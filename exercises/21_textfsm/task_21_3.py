# -*- coding: utf-8 -*-
"""
Задание 21.3

Создать функцию parse_command_dynamic.

Параметры функции:
* command_output - вывод команды (строка)
* attributes_dict - словарь атрибутов, в котором находятся такие пары ключ-значение:
 * 'Command': команда
 * 'Vendor': вендор
* index_file - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"
* templ_path - каталог, где хранятся шаблоны. Значение по умолчанию - "templates"

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br.
"""
from textfsm import clitable

def parse_command_dynamic(command_output, attributes_dict, index_file='index', templ_path='templates'):
    cli = clitable.CliTable(index_file, templ_path)
    cli.ParseCmd(command_output, attributes_dict)
    header = list(cli.header)
    data = [list(row) for row in cli]
    result = [dict(zip(header, row)) for row in data]
    return result

if __name__ == '__main__':
    with open('output/sh_ip_int_br.txt') as f:
        output = f.read()
    attributes = {'Command': 'sh ip int br', 'Vendor': 'cisco_ios'}
    print(parse_command_dynamic(output, attributes))