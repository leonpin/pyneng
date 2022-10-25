# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping (запуск ping через subprocess).
IP-адрес считается доступным, если выполнение команды ping отработало с кодом 0 (returncode).
Нюансы: на Windows returncode может быть равен 0 не только, когда ping был успешен,
но для задания нужно проверять именно код. Это сделано для упрощения тестов.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import subprocess
from pprint import pprint

def ping_ip_addresses(ip_list):
    avail = []
    unavail = []
    for ip in ip_list:
        reply = subprocess.run(['ping', '-c', '1', ip],
                               stdout=subprocess.DEVNULL, encoding='utf-8')
        if reply.returncode:
            unavail.append(ip)
        else:
            avail.append(ip)
    return avail, unavail

if __name__ == '__main__':
    t = ping_ip_addresses(['10.0.0.1', '8.8.8.8', '192.168.1.1'])
    pprint(f'avail {t[0]}, unavail {t[1]}')

