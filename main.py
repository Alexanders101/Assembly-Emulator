#!/usr/bin/env python3
from utils import *
from memory import Memory
from register import Register
from stack import Stack
from commands import masm_commands


class VarType:
    """
    Stores the named information about variable types

    ...
    Parameters
    ----------
    name : str
        Data-type name. This is what the user type ex. WORD
    size : int
        Size of data-type in bytes
    signed : bool
        Whether or not the variable type should be interpreted as signed

    Attributes
    ----------
    name : str
        Data-type name. This is what the user type ex. WORD
    size : int
        Size of data-type in bytes
    signed : bool
        Whether or not the variable type should be interpreted as signed
    bits : int
        Size of data-type in bits
    _converted : dict(tuple, str, type)
        Storage for all of the possible conversions of the data-type
    type : type
        Numpy type for the given data-type
    word : str
        Same as name
    det : tuple(int, bool)
        Contains the size and signed attributes

    """
    def __init__(self, name, size, signed):
        self.name = name
        self.bytes = size
        self.bits = size * 8
        self.signed = signed
        self._converted = variable_all(self.bytes, self.signed)

    @property
    def type(self):
        return self._converted['type']

    @property
    def word(self):
        return self._converted['word']

    @property
    def det(self):
        return self._converted['det']


class Processor(Component):
    """
    Holder type for all processor commands

    ...
    Parameters
    ----------
    command_list : dict
        List of commands with their callable names as the keys
    """
    def __init__(self, command_list):
        super(Processor, self).__init__('Processor')
        for k, v in command_list.items():
            setattr(self, k, v)


class Computer:
    """
    Simulation superclass

    ...
    Parameters
    ----------
    mem_size : int
        Size of memory in bytes
    stack_size : int
        Size of stack in levels.
    command_list : str
        Instruction list to load.

    Attributes
    ----------
    cpu : Processor
        Holds the instructions for the computer.
    mem : Memory
        Memory holding variables of the computer.
    reg : dict(name: Register)
        Dictionary holding the registers of the computer, indexed by their names.
    stack : Stack
        The processor stack.
    vt : dict(name: VarType)
        Stores all of the possible variable types for the computer
    """
    vt = {
        'BYTE'  : VarType('BYTE', 1, False),
        'SBYTE' : VarType('SBYTE', 1, True),
        'WORD'  : VarType('WORD', 2, False),
        'SWORD' : VarType('SWORD', 2, True),
        'DWORD' : VarType('DWORD', 4, False),
        'SDWORD': VarType('SDWORD', 4, True),
        'QWORD' : VarType('QWARD', 8, False)
    }

    @staticmethod
    def __make_registers():
        """
        Creates the 32-bit register set

        ...
        Returns
        -------
        A dictionary of 32 bit registers, indexed by their names.
        """
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

        self.cpu = Processor(command_list)
        self.mem = Memory(mem_size)
        self.reg = self.__make_registers()
        self.stack = Stack(stack_size)


if __name__ == "__main__":
    comp = Computer()
