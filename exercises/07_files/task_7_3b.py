# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
with open('CAM_table.txt','r') as f:
    v=input('VLAN: ')
    result=[]
    for line in f:
        line = line.split()
        if line and line[0] == v:
            vlan, mac, _, port = line
            result.append([int(vlan),mac,port])
    result = sorted(result)
    for line in result:
        print('{:<8} {} {:>10}'.format(*line))