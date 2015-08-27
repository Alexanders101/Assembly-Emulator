import numpy as np
from main import Component

max_value = {
	1 : 255,
	2 : 65535,
	3 : 4294967295,
	4 : 18446744073709551615
}
def split_number(number, size):
	if abs(number) > max_value[size]:
		raise Exception('{0} is too big for size {1}'.format(number, size))

	binary = np.binary_repr(number, width=(size*8))[:size*8]
	print(binary)
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


class Memory(Component):
	def __init__(self, size):
		super(Memory, self).__init__('Memory')
		self.memory = np.zeros((size,), dtype=np.int8)

x = split_number(255, 2)
print(x)
print(combine_number(x,True))