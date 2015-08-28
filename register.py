from utils import *


class Register(Component, Active):

    def __init__(self, name, use="", size=32, subregister=None):
        super(Register, self).__init__('Register')
        # Component.__init__(self, 'Register')
        self.name = name
        self.use = use
        self.bits = size
        self.size = size // 8
        if subregister is None:
            self._range = slice(0, size // 8)
            self._value = np.zeros((size // 8,), dtype=np.uint8)
        else:
            self._range = subregister[0]
            self._value = subregister[1]

    @property
    def value(self):
        return combine_number(self._value[self._range])

    @value.setter
    def value(self, val):
        self._value[self._range] = split_number(val, self.size)

    def make_subregisters(self, *names):
        start = int(self._range.start)
        stop = int(self._range.stop)
        mid = int(start + ((stop - start) // 2))
        ranges = (slice(start, mid),
                  slice(mid, stop))
        sub_one = Register(
            names[0], use=self.use, size=self.bits // 2, subregister=(ranges[0], self._value))
        sub_two = Register(
            names[1], use=self.use, size=self.bits // 2, subregister=(ranges[1], self._value))
        return (sub_one, sub_two)

    @property
    def mem(self):
        return self._value[self._range]

    def __repr__(self):
        return "{}\n{}\n{}".format(self.bits, self.value, self._value[self._range])

    def __str__(self):
        return "{0}\nUsage: {1}\nSize: {2} bits\nCurrent Value: {3}".format(self.name, self.use, self.bits, hex(self.value, self.bits))

    def __call__(self, val=None):
        if val is not None:
            self.value = val
        return self.value



# eax = Register('eax')
# _, ax = eax.make_subregisters('_', 'ax')
# ah, al = ax.make_subregisters('ah', 'al')
# print(eax())
# print(eax(5))
# print(eax)
# al(255)
# print(repr(eax))
# al += 1
# print(repr(eax))
