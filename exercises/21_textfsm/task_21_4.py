# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""
import yaml
from textfsm import clitable
from netmiko import ConnectHandler

def send_and_parse_show_command(device_dict, command, templates_path, index='index'):
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        output = ssh.send_command(command)
    clit = clitable.CliTable(index, templates_path)
    clit.ParseCmd(output, {'Command':command})
    header = list(clit.header)
    data = [list(row) for row in clit]
    result = [dict(zip(header, row)) for row in data]
    return result

if __name__ == '__main__':
    command = 'sh ip int br'
    templates_path = 'templates'
    with open('devices.yaml') as f:
        device_dict = yaml.safe_load(f)
    print(send_and_parse_show_command(device_dict[0], command, templates_path))