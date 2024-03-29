# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

"""
import telnetlib
from textfsm import clitable

class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b'Username')
        self._write_line(username)
        self.telnet.read_until(b'Password')
        self._write_line(password)
        self._write_line('enable')
        self.telnet.read_until(b'Password')
        self._write_line(secret)
        self.telnet.read_until(b'#', timeout=5)

    def _write_line(self, line):
        self.telnet.write(line.encode('ascii') + b'\n')

    def send_show_command(self, command, parse=True, templates='templates', index='index'):
        self._write_line(command)
        output = self.telnet.read_until(b'#', timeout=5).decode('ascii')
        if parse:
            clit = clitable.CliTable(index, templates)
            clit.ParseCmd(output, {'Command': command})
            output = [dict(zip(clit.header, row)) for row in clit]
        return output

    def send_config_commands(self, commands):
        output = ''
        if type(commands) == str:
            commands = [commands]
        for command in ['conf t', *commands, 'end']:
            self._write_line(command)
            output += self.telnet.read_until(b'#', timeout=5).decode('ascii')
        return output

    def con_close(self):
        self.telnet.close()

if __name__ == '__main__':
    r1_params = {
    'ip': '192.168.100.1',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco'}
    r1 = CiscoTelnet(**r1_params)
    print(r1.send_config_commands(['alias configure sh do sh', 'alias exec ospf sh run | s ^router ospf']))
    r1.con_close()