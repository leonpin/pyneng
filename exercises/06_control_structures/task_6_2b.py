# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
while True:
    try:
        addr = [int(str) for str in input('Введите адрес: ').split('.') if int(str)<=255]
    except ValueError:
            print('Неправильный IP-адрес')
            continue
    if len(addr)==4:
        if 0<addr[0]<=223:
            print('unicast')
        elif 224<=addr[0]<=239:
            print('multicast')
        elif addr[0]==addr[1]==addr[2]==addr[3]==255:
            print('local broadcast')
        elif addr[0]==addr[1]==addr[2]==addr[3]==0:
            print('unassigned')
        else:
            print('unused')
        break
    else:
        print('Неправильный IP-адрес')