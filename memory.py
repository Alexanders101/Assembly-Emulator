from utils import *

class VariableNotInitialized(Exception):
    pass

class VariableNotDefined(Exception):
    pass

class VariableAlreadyDefined(Exception):
	    pass

class Variable(Active):
	def __init__(self, value, name, offset, size, signed, initialized):
		self._value = variable_det_to_type(size, signed)(value)
		self.offset = offset
		self.size = size
		self.signed = signed
		self.name = name
		self.init = initialized

	@property
	def value(self):
		if not self.init:
		 	raise VariableNotInitialized('Variable {0} has not been initialized'.format(self.name))
		return self._value
	@value.setter
	def value(self, other):
		self._value = other

	def __repr__(self):
		return "{}, {}, {}, {}".format(self.value, self.init, self.size, self.signed)
	def __str__(self):
		base = "{} {}".format(variable_det_to_word(self.size, self.signed), self.name)
		if self.init:
			base = "{} = {}".format(base, self.value)
		return base
	def __call__(self):
		return self.value


class Memory(Component):
	def __init__(self, size):
		# super(Memory, self).__init__('Memory')
		Component.__init__(self, 'Memory')
		self.memory = np.zeros((size,), dtype=np.uint8)
		self.offset = 0
		self.variables = {}

	def __call__(self, name, *args, **xargs):
		if len(args) == 0 and len(xargs) == 0:
			return self.get(name)
		else:
			self.set(name, *args, **xargs)

	def __repr__(self):
		return str(self.variables)

	def __str__(self):
		return "Currently {} variables in memory".format(len(self.variables))

	def set(self, name, variable=None, size=None, signed=False):
		# Changing and existing variable
		if size is None:
			try:
				curr, size, signed, init = self.variables[name]
			except KeyError:
				raise Exception('A new variable needs size')

		# Creating a new variable
		else:
			if name in self.variables:
				raise VariableAlreadyDefined()
			# update the offset
			curr = self.offset
			self.offset += size

		# Not initializing, value remains 0
		if variable is None:
			if name in self.variables:
				raise VariableAlreadyDefined()
			init = False

		# Setting value in memory
		else:
			if isinstance(variable, Active):
				variable = variable.value
			variable = variable_det_to_type(size, signed)(variable)
			value = split_number(variable, size)
			self.memory[curr:curr+size] = value
			init = True

		# Adding variable to variable list
		self.variables[name] = (curr, size, signed, init)

	def __getitem__(self, key):
		return self.get(key)
	@dispatch(str, object)
	def __setitem__(self, key, value):
		self.set(key, value.value)
	@dispatch(str, int)
	def __setitem__(self, key, value):
		if key not in self.variables:
			self.set(key, value, 4)
		else:
			self.set(key, value)

	def get(self, name):

		try:
			offset, size, signed, init = self.variables[name]
		except KeyError:
			raise VariableNotDefined('Variable {0} has not been defined'.format(name))

		value = self.memory[offset:offset+size]
		return Variable(combine_number(value, signed), name, offset, size, signed, init)

	def dell(self, name):
		try:
			offset, size, signed, init = self.variables[name]
		except KeyError:
			raise VariableNotDefined()

		self.memory[offset:offset+size] = [0]*size
		del self.variables[name]


if __name__ == "__main__":
	mem = Memory(1024)
	mem('x', size=1, signed=1)
	mem('y', size=2, signed=0)
	mem('z', size=4, signed=1)

	mem['x'] = 127
	mem['y'] = 5723
	mem['z'] = 111


	print(mem['x'])
	print(mem['y'])
	print(mem['z'])
