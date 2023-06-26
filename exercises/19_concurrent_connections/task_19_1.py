# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

def ping_ip(ip):
    reply = subprocess.run(['ping', '-c', '2', '-n', ip], stdout=subprocess.DEVNULL)
    return reply.returncode == 0

def ping_ip_addresses(ip_list, limit=3):
    reachable = []
    unreachable = []
    with ThreadPoolExecutor(max_workers=limit) as e:
        results = e.map(ping_ip, ip_list)
        for ip, reply in zip(ip_list, results):
            if reply:
                reachable.append(ip)
            else:
                unreachable.append(ip)
    return reachable, unreachable

if __name__ == "__main__":
    addr_list = ['192.168.241.1', '192.168.100.2', '192.168.100.5']
    print(ping_ip_addresses(addr_list))