# -*- coding: utf-8 -*-
"""
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона,
например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список,
где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список, в котором содержатся IP-адреса
и/или диапазоны IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные
адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только
последний октет адреса.

Функция возвращает список IP-адресов.

Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

"""

import ipaddress
import re

def convert_ranges_to_ip_list(ip_list):
    result = []


    for ip in ip_list:
        addr = []
        if '-' in ip:
            ip1, ip2 = ip.split('-')
            if '.' not in ip2:
                ip2 = re.search(r'\d\.\d\.\d\.',ip1).group()+ip2

                #ip2 = f"{'.'.join(ip1.split('.')[:-1])}.{ip2}"
            ip1 = ipaddress.ip_address(ip1)
            ip2 = ipaddress.ip_address(ip2)
            for i in range(int(ip1), int(ip2)+1):
                addr.append(str(ipaddress.ip_address(i)))
        else:
            addr.append(ip)
        result.extend(addr)
    return result

print(convert_ranges_to_ip_list(['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']))