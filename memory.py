from utils import *

class VariableNotInitialized(Exception):
    pass

class VariableNotDefined(Exception):
    pass

class VariableAlreadyDefined(Exception):
	    pass

class Memory(Component):
	def __init__(self, size):
		# super(Memory, self).__init__('Memory')
		Component.__init__(self, 'Memory')
		self.memory = np.zeros((size,), dtype=np.uint8)
		self.offset = 0
		self.variables = {}

	def set(self, name, variable=None, size=None, signed=False):
		if size is None:
			try:
				curr, size, signed, init = self.variables[name]
			except KeyError:
				raise Exception('A new variable needs size')
		else:
			if name in self.variables:
				raise VariableAlreadyDefined()
			curr = self.offset
			self.offset += size

		if variable is None:
			if name in self.variables:
				raise VariableAlreadyDefined()
			init = False
		else:
			value = split_number(variable, size)
			self.memory[curr:curr+size] = value
			init = True

		self.variables[name] = (curr, size, signed, init)
	def get(self, name):
		try:
			offset, size, signed, init = self.variables[name]
		except KeyError:
			raise VariableNotDefined('Variable {0} has not been defined'.format(name))

		if not init:
			raise VariableNotInitialized('Variable {0} has not been initialized'.format(name))

		value = self.memory[offset:offset+size]
		return combine_number(value, signed)

	def dell(self, name):
		try:
			offset, size, signed, init = self.variables[name]
		except KeyError:
			raise VariableNotDefined()

		self.memory[offset:offset+size] = [0]*size
		del self.variables[name]


if __name__ == "__main__":
	mem = Memory(1024)
	mem.set('x', size=1)
	mem.set('x', 5)
	mem.set('x', mem.get('x') + 5)
	mem.get('x')
	mem.get('x')

	mem.dell('x')
