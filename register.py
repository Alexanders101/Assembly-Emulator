#!/usr/bin/env python3
from utils import *


class Register(Component, Active):
    """
    Simulate the cpu registers

    ...
    Parameters
    ----------
    name : string
        The name of the current register
    use : string
        The specialized usage of the register, used for education
    size : int
        The size of the register in bits
    subregister
        For creating a subregister, only used when creating register
        from make_subregisters method

    Attributes
    ----------
    name : str
        The name of the current register
    use : str
        The specialized usage of the register, used for education
    bits : int
        The size of the register in bits
    size : int
        The size of the register in bytes
    _range : slice
        The range the current register has on the main memory array
    _value : ndarray
        The current value of the register stored as an array of bytes
    value : ?
        The current value of the register converted into the registers dtype
    mem : ndarray
        Accessor property for the _value attribute

    Methods
    -------
    make_subregisters(high_reg, low_reg)
        Creates 2 subregisters from the current register that share the same base memory.

    """

    def __init__(self, name: str, use: str="", size: int=32, subregister: tuple=None):
        """
        Parameters
        ----------
        name : string
            The name of the current register
        use : string
            The specialized usage of the register, used for education
        size : int
            The size of the register in bits
        subregister
            For creating a subregister, only used when creating register
            from make_subregisters method
        """
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

    @property
    def mem(self):
        return self._value[self._range]

    def make_subregisters(self, high: str, low: str):
        """
        Create linked sub-registers for a larger register.

        Parameters
        ----------
        high : str
            Name of the upper register.
        low : str
            Name of the lower register.

        Returns
        -------
        high_register : Register
            The upper register.
        low_register : Register
            The lower register.

        Notes
        -----
        The sub-registers returned will be half the size of the parent register.
        They will also share memory between themselves and their parents. Changing
        the lower or upper sub-registers will affect the lower and upper bytes of the
        parent respectively.

        Examples
        --------
        >>> eax = Register(name='eax')
        >>> eax.value = 20
        32
        20
        [ 0  0  0 20]
        >>> _, ax = eax.make_subregisters('_', 'ax')
        >>> ax
        16
        20
        [ 0 20]
        >>> ax.value = 50
        >>> eax
        32
        50
        [ 0  0  0 50]

        In this example, we create the extended 32-bit eax register and then
        create a 16-bit sub-register named ax. Notice how the memory is shared
        between the two: editing one of the registers will affect the other.
        """
        start = self._range.start
        stop = self._range.stop
        mid = start + ((stop - start) // 2)
        ranges = (slice(start, mid),
                  slice(mid, stop))
        high_register = Register(
            high, use=self.use, size=self.bits // 2, subregister=(ranges[0], self._value))
        low_register = Register(
            low, use=self.use, size=self.bits // 2, subregister=(ranges[1], self._value))
        return high_register, low_register

    def __repr__(self):
        return "{}\n{}\n{}".format(self.bits, self.value, self._value[self._range])

    def __str__(self):
        return "{0}\nUsage: {1}\nSize: {2} bits\nCurrent Value: {3}".format(self.name, self.use, self.bits,
                                                                            hex(self.value, self.bits))

    def __call__(self, val=None):
        if val is not None:
            self.value = val
        return self.value


if __name__ == '__main__':
    eax = Register('eax')
    _, ax = eax.make_subregisters('_', 'ax')
    ah, al = ax.make_subregisters('ah', 'al')
