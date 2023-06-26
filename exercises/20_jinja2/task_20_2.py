# -*- coding: utf-8 -*-
"""
Задание 20.2

Создать шаблон templates/cisco_router_base.txt.

В шаблон templates/cisco_router_base.txt должно быть включено содержимое шаблонов:
* templates/cisco_base.txt
* templates/alias.txt
* templates/eem_int_desc.txt

При этом, нельзя копировать текст шаблонов.

Проверьте шаблон templates/cisco_router_base.txt, с помощью
функции generate_config из задания 20.1. Не копируйте код функции generate_config.

В качестве данных, используйте информацию из файла data_files/router_info.yml

"""
from task_20_1 import generate_config
import yaml

template = """
{% include 'cisco_base.txt' %}
{% include 'alias.txt' %}
{% include 'eem_int_desc.txt' %}
"""
filename = 'templates/cisco_router_base.txt'
with open(filename, 'w') as f:
    f.write(template)
with open('data_files/router_info.yml') as f:
    data = yaml.safe_load(f)
print(generate_config(filename, data))