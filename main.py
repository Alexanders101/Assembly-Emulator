#!/usr/bin/env python3
import numpy as np
from multipledispatch import dispatch
from commands import masm_commands

class VarType():
	def __init__(self, name, size):
		self.name = name
		self.byte = size
		self.bit = size * 8


class Component():
	def __init__(self, name, *args, **xargs):
		self.name = name
class Proccessor(Component):
	def __init__(self, command_list):
		super(Proccessor, self).__init__('Proccessor')
		for k, v in command_list.items():
			setattr(self, k, v)

class Register():
	def __init__(self, name, use="", size = 32):
		self.name = name
		self.use = use
		self.size = size
		self.dtype = eval("np.int{0}".format(size))
		self.value = self.dtype(0)
		self.value = 0

	def __repr__(self):
		return "{0}\nUsage: {1}\nSize: {2} bits\nCurrent Value: {3}".format(self.name, self.use, self.size, hex(self.value))

	def __str__(self):
		return "{0}\nUsage: {1}\nSize: {2} bits\nCurrent Value: {3}".format(self.name, self.use, self.size, hex(self.value))

	@dispatch(int)
	def __add__(self, other):
		return self.value + self.dtype(other)

	@dispatch(int)
	def __iadd__(self, other):
		self.value += self.dtype(other)
		return self.value

	@dispatch(object)
	def __add__(self, other):
		return self.value + self.dtype(other.value)
	@dispatch(object)
	def __iadd__(self, other):
		self.value += self.dtype(other.value)
		return self.value



class Computer():
	vt = {'BYTE' : VarType('BYTE', 1),
		  'WORD' : VarType('VarType', 2),
		  'DWORD': VarType('DWORD', 4),
		  'QWORD': VarType('QWARD', 8)}

	rg = {'eax' : Register('eax'),
    	  'ebx' : Register('ebx'),
    	  'ecx' : Register('ecx'),
          'edx' : Register('edx'),
          'ebp' : Register('ebp'),
          'esi' : Register('esi'),
          'edi' : Register('edi'),
          'esp' : Register('esp')}

	def __init__(self, command_list='masm'):
		if command_list is 'masm':
			command_list = masm_commands

		self.cpu = Proccessor(command_list)


if __name__ == "__main__":
	cpu = Proccessor(masm_commands)
	eax = Register('eax')
	ebx = Register('ebx')
	cpu.MOV(ebx, 5)
	cpu.ADD(eax, ebx)
	print(eax)

