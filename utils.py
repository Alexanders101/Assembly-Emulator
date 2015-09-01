#!/usr/bin/env python3
import warnings
import numpy as np
from multipledispatch import dispatch
from copy import deepcopy
from errors import *

warnings.filterwarnings("ignore")
old_hex = hex


class Component:
    """
    Main Superclass for all of the components of a computer.

    ...
    Parameters
    ----------
    name : str
        Name of a given component.

    """

    def __init__(self, name: str):
        self.name = name


class Active:
    """
    Main superclass for all components that hold values
    and requires to be operated on other such components.

    ...
    Extended Summary
    ----------------
    This class provides all of the comparison and mathematical
    operation magic methods to classes that inherit it.
    Every magic method has two version: one between self
    and a number, and one between self and another Active.

    In order for these methods to work, classes that inherit Active
    must implement a 'value' property or attribute that return a
    numeric value when called.

    Notes
    -----
    All magic methods raise IncompatibleVariableSizes when calling
    one of the methods with two Actives that hold variables of two
    different sizes
    """

    @dispatch((int, np.generic))
    def __add__(self, other):
        temp = deepcopy(self)
        temp.value = temp.value + type(self.value)(other)
        return temp

    @dispatch((int, np.generic))
    def __iadd__(self, other):
        self.value = self.value + type(self.value)(other)
        return self

    @dispatch((int, np.generic))
    def __sub__(self, other):
        temp = deepcopy(self)
        temp.value = temp.value - type(self.value)(other)
        return temp

    @dispatch((int, np.generic))
    def __isub__(self, other):
        self.value = self.value - type(self.value)(other)
        return self

    @dispatch((int, np.generic))
    def __mul__(self, other):
        temp = deepcopy(self)
        temp.value = temp.value * type(self.value)(other)
        return temp

    @dispatch((int, np.generic))
    def __imul__(self, other):
        self.value = self.value * type(self.value)(other)
        return self

    @dispatch((int, np.generic))
    def __truediv__(self, other):
        temp = deepcopy(self)
        temp.value = temp.value // type(self.value)(other)
        return temp

    @dispatch((int, np.generic))
    def __itruediv__(self, other):
        self.value = self.value // type(self.value)(other)
        return self

    @dispatch(Component)
    def __add__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        temp = deepcopy(self)
        temp.value = temp.value + type(temp.value)(other.value)
        return temp

    @dispatch(Component)
    def __iadd__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        self.value = self.value + type(self.value)(other.value)
        return self

    @dispatch(Component)
    def __sub__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        temp = deepcopy(self)
        temp.value = temp.value - type(temp.value)(other.value)
        return temp

    @dispatch(Component)
    def __isub__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        self.value = self.value - type(self.value)(other.value)
        return self

    @dispatch(Component)
    def __mul__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        temp = deepcopy(self)
        temp.value = temp.value * type(temp.value)(other.value)
        return temp

    @dispatch(Component)
    def __imul__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        self.value = self.value * type(self.value)(other.value)
        return self

    @dispatch(Component)
    def __truediv__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        temp = deepcopy(self)
        temp.value = temp.value // type(temp.value)(other.value)
        return temp

    @dispatch(Component)
    def __itruediv__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        self.value = self.value // type(self.value)(other.value)
        return self


max_value = {
    1: 255,
    2: 65535,
    4: 4294967295,
    8: 18446744073709551615
}


def binary(number, size: int=32) -> str:
    """
    Converts a number into its binary string representation.

    Parameters
    ----------
    number : int:
        Number to convert.
    size : int, optional
        Size of binary string in bits.

    Returns
    -------
    str
        The binary representation of the number.

    """
    binary = np.binary_repr(number, width=size)[:size]
    return binary


def binary_arr(arr: list) -> str:
    """
    Convert an array of 8-bit integers
    into the full binary representation.

    Parameters
    ----------
    arr : list(int)
        List of 8-bit integers.

    Returns
    -------
    str
        Binary representation of the array.

    """

    return ''.join([binary(val, 8) for val in arr])


def split_number(number, size: int) -> str:
    """
    Split a number into an 8-bit array for easy storage in memory.

    Parameters
    ----------
    number : int
        Number to convert.
    size : [1, 2, 4, 8]
        Size of the list in bytes

    Returns
    -------
    list(np.int8)
        The byte list representation of the number.

    Raises
    ------
    ValueError
        If the number given is greater than the maximum value allowed by the array size.
    InvalidSize
        The size given is not in the list of allowed sizes.
    """

    try:
        if abs(number) > max_value[size]:
            raise ValueError('{0} is too big for size {1}'.format(number, size))
    except KeyError:
        raise InvalidSize(size)

    binary = np.binary_repr(number, width=(size * 8))[:size * 8]
    binary = [binary[curr * 8:(curr + 1) * 8] for curr in range(size)]
    return [eval('0b{0}'.format(num)) for num in binary]


def combine_number(memory_seg, signed: bool=False) -> np.generic:
    """
    Combine a byte array generated by split_number() back into a number.

    Parameters
    ----------
    memory_seg : list(int)
        Array containing the values of each byte.
    signed : [False, True], optional
        Whether or not the final number is signed or unsigned.

    Returns
    -------
    numpy integer type
        Value of the byte array in its appropriate numpy integer format.

    """

    binary = [np.binary_repr(number, width=8) for number in memory_seg]
    binary = ''.join(binary)
    size = len(memory_seg)
    return variable_det_to_type(size, signed)(eval('0b{}'.format(binary)))


def hex(value, size: int=8) -> str:
    """
    Updated version of default python hex function
    that allows the output to be a fixed size.

    Parameters
    ----------
    value : any
        Value to convert.
    size : int
        Size of the hex number in digits.

    Returns
    -------
    str
        The hex representation of the value.

    """

    value = old_hex(value)
    current_length = len(value[2:])
    extra = size - current_length
    if extra <= 0:
        return value

    return '0x{0}{1}'.format('0' * extra, value[2:])


def variable_det_to_word(size: int, signed: bool) -> str:
    """
    Convert a description of a variable type to the
    assembly word description of the type.
    
    Parameters
    ----------
    size : [1,2,4,8]
        Size of variable type in bytes.
    signed : [True, False]
        Whether or not the variable is signed.
    
    Returns
    -------
    Word : str
        Assembly word form of variable.
    
    """
    
    size = {1: 'BYTE',
            2: 'WORD',
            4: 'DWORD',
            8: 'QWORD'}[size]
    if signed:
        size = "S{}".format(size)
    return size


def variable_det_to_type(size: int, signed: bool) -> type:
    """
    Convert a description of a variable type to the
    numpy type representing the same type.

    Parameters
    ----------
    size : [1,2,4,8]
        Size of variable type in bytes.
    signed : [True, False]
        Whether or not the variable is signed.

    Returns
    -------
    _type : type
        Numpy type matching variable description.

    """
    word = {1: 'int8',
            2: 'int16',
            4: 'int32',
            8: 'int64'}[size]
    if not signed:
        word = "u{}".format(word)
    return eval('np.{}'.format(word))


def variable_word_to_type(word: str) -> type:
    """
    Convert the assembly word description of a variable type
    into the equivalent numpy type.

    Parameters
    ----------
    word : str
        Assembly word for the variable type.

    Returns
    -------
    _type : type
        Numpy type matching variable description.

    """

    word = word.upper()
    signed = False
    if word[0] == 'S':
        signed = True
        word = word[1:]

    word = {'BYTE' : 'int8',
            'WORD' : 'int16',
            'DWORD': 'int32',
            'QWORD': 'int64'}[word]
    if not signed:
        word = "u{}".format(word)

    return eval('np.{}'.format(word))


def variable_word_to_det(word: str) -> tuple:
    """
    Convert the assembly word description of a variable type
    into the description of the variable type.

    Parameters
    ----------
    word : str
        Assembly word for the variable type.

    Returns
    -------
    size : int
        Size of variable type in bytes
    signed : bool
        Whether or not the variable type is signed

    """
    word = word.upper()
    signed = False
    if word[0] == 'S':
        signed = True
        word = word[1:]

    size = {'BYTE' : 1,
            'WORD' : 2,
            'DWORD': 4,
            'QWORD': 8}[word]

    return size, signed


def variable_type_to_det(_type):
    """
    Convert the numpy type into the description
    of the variable type.

    Parameters
    ----------
    _type : type
        Numpy type equivalent to the variable type

    Returns
    -------
    size : int
        Size of variable type in bytes
    signed : bool
        Whether or not the variable type is signed

    """
    det = str(_type)[14:].split("'")[0]
    signed = True
    if det[0] == 'u':
        signed = False
        det = det[1:]

    size = {'int8' : 1,
           'int16': 2,
           'int32': 4,
           'int64': 8}[det]

    return size, signed


def variable_type_to_word(_type):
    """
    Convert a description of a variable type to the
    assembly word description of the type.

    Parameters
    ----------
    size : [1,2,4,8]
        Size of variable type in bytes.
    signed : [True, False]
        Whether or not the variable is signed.

    Returns
    -------
    Word : str
        Assembly word form of variable.

    """
    word = str(_type)[14:].split("'")[0]
    signed = True
    if word[0] == 'u':
        signed = False
        word = word[1:]

    word = {'int8' : 'BYTE',
            'int16': 'WORD',
            'int32': 'DWORD',
            'int64': 'QWORD'}[word]

    if signed:
        word = 'S{}'.format(word)

    return word


def variable_all(*args, **kwargs):
    if (len(args) + len(kwargs)) == 2:
        word = variable_det_to_word(*args, **kwargs)
        _type = variable_det_to_type(*args, **kwargs)
        try:
            size = kwargs['size']
        except KeyError:
            size = args[0]

        try:
            signed = kwargs['signed']
        except KeyError:
            signed = args[1]

        return {'word': word,
                'type': _type,
                'det' : (size, bool(signed))}

    elif len(kwargs) == 1:
        try:
            var = kwargs['word']
        except KeyError:
            var = kwargs['_type']
            word_conv = False
        else:
            word_conv = True

    elif len(args) == 1:
        var = args[0]
        if isinstance(var, str):
            word_conv = True
        else:
            word_conv = False
    else:
        raise Exception('No match found for conversion')

    if word_conv:
        word = var.upper()
        _type = variable_word_to_type(word)
        det = variable_word_to_det(word)
    else:
        _type = var
        word = variable_type_to_word(_type)
        det = variable_type_to_det(_type)

    return {'word': word,
            'type': _type,
            'det' : det}
