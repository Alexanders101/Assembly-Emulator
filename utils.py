import numpy as np
from multipledispatch import dispatch
old_hex = hex

class Component():
	def __init__(self, name, *args, **xargs):
		self.name = name

max_value = {
	1 : 255,
	2 : 65535,
	3 : 4294967295,
	4 : 18446744073709551615
}

def binary(number, size=32):
	binary = np.binary_repr(number, width=(size))[:size]
	return binary

def binary_arr(arr):
	return ''.join([binary(val, 8) for val in arr])

def split_number(number, size):
	if abs(number) > max_value[size]:
		raise Exception('{0} is too big for size {1}'.format(number, size))

	binary = np.binary_repr(number, width=(size*8))[:size*8]
	# rint(binary)
	binary = [binary[curr*8:(curr+1)*8] for curr in range(size)]
	return [eval('0b{0}'.format(num)) for num in binary]

def combine_number(memory_seg, signed = False):
	binary = [np.binary_repr(number, width=8) for number in memory_seg]
	binary = ''.join(binary)
	if signed:
		sign, binary = binary[0], binary[1:]
		sign = -1 if sign == '1' else 1
	else:
		sign = 1

	return (sign * eval('0b{0}'.format(binary)))

def hex(value, size=8):
	value = old_hex(value)
	current_length = len(value[2:])
	extra = size - current_length
	if extra <= 0:
		return value

	return '0x{0}{1}'.format('0'*extra, value[2:])
