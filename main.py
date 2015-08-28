#!/usr/bin/env python3
from utils import *
from memory import Memory
from register import Register
from stack import Stack
from commands import masm_commands


class VarType():

    def __init__(self, name, size):
        self.name = name
        self.byte = size
        self.bit = size * 8


class Proccessor(Component):

    def __init__(self, command_list):
        super(Proccessor, self).__init__('Proccessor')
        for k, v in command_list.items():
            setattr(self, k, v)


class Computer():
    vt = {'BYTE': VarType('BYTE', 1),
          'WORD': VarType('VarType', 2),
          'DWORD': VarType('DWORD', 4),
          'QWORD': VarType('QWARD', 8)}

    def __make_registers(self):
        reg = {'eax': Register('eax'),
               'ebx': Register('ebx'),
               'ecx': Register('ecx'),
               'edx': Register('edx'),
               'ebp': Register('ebp'),
               'esi': Register('esi'),
               'edi': Register('edi'),
               'esp': Register('esp')}
        _, reg['ax'] = reg['eax'].make_subregisters('_', 'ax')
        reg['ah'], reg['al'] = reg['ax'].make_subregisters('ah', 'al')

        _, reg['bx'] = reg['ebx'].make_subregisters('_', 'bx')
        reg['bh'], reg['bl'] = reg['bx'].make_subregisters('bh', 'bl')

        _, reg['cx'] = reg['ecx'].make_subregisters('_', 'cx')
        reg['ch'], reg['cl'] = reg['cx'].make_subregisters('ch', 'cl')

        _, reg['dx'] = reg['edx'].make_subregisters('_', 'dx')
        reg['dh'], reg['dl'] = reg['dx'].make_subregisters('dh', 'dl')

        _, reg['bp'] = reg['ebp'].make_subregisters('_', 'bp')
        _, reg['si'] = reg['esi'].make_subregisters('_', 'si')
        _, reg['di'] = reg['edi'].make_subregisters('_', 'di')
        _, reg['sp'] = reg['esp'].make_subregisters('_', 'sp')

        return reg

    def __init__(self, mem_size=1024, stack_size=1024, command_list='masm'):
        if command_list is 'masm':
            command_list = masm_commands

        self.cpu = Proccessor(command_list)
        self.mem = Memory(mem_size)
        self.reg = self.__make_registers()
        self.stack = Stack(stack_size)


if __name__ == "__main__":
    comp = Computer()
