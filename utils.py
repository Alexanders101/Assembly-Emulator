import numpy as np
from multipledispatch import dispatch
from copy import copy, deepcopy
import warnings
warnings.filterwarnings("ignore")
old_hex = hex


class InvalidSize(Exception):
    pass
class IncompatibleVariableSizes(Exception):
    pass

class Component():

    def __init__(self, name, *args, **xargs):
        self.name = name

max_value = {
    1: 255,
    2: 65535,
    4: 4294967295,
    8: 18446744073709551615
    }

def binary(number, size=32):
    binary = np.binary_repr(number, width=(size))[:size]
    return binary


def binary_arr(arr):
    return ''.join([binary(val, 8) for val in arr])


def split_number(number, size):
    try:
        if abs(number) > max_value[size]:
            raise Exception('{0} is too big for size {1}'.format(number, size))
    except KeyError:
        raise InvalidSize(size)
    binary = np.binary_repr(number, width=(size * 8))[:size * 8]
    binary = [binary[curr * 8:(curr + 1) * 8] for curr in range(size)]
    return [eval('0b{0}'.format(num)) for num in binary]


def combine_number(memory_seg, signed=False):
    binary = [np.binary_repr(number, width=8) for number in memory_seg]
    binary = ''.join(binary)
    size = len(memory_seg)
    return variable_det_to_type(size, signed)(eval('0b{}'.format(binary)))



def hex(value, size=8):
    value = old_hex(value)
    current_length = len(value[2:])
    extra = size - current_length
    if extra <= 0:
        return value

    return '0x{0}{1}'.format('0' * extra, value[2:])

class Active():

    @dispatch(int)
    def __add__(self, other):
        temp = deepcopy(self)
        temp.value = temp.value + type(self.value)(other)
        return temp

    @dispatch(int)
    def __iadd__(self, other):
        self.value = self.value + type(self.value)(other)
        return self

    @dispatch(int)
    def __sub__(self, other):
        temp = deepcopy(self)
        temp.value = temp.value - type(self.value)(other)
        return temp

    @dispatch(int)
    def __isub__(self, other):
        self.value = self.value - type(self.value)(other)
        return self

    @dispatch(int)
    def __mul__(self, other):
        temp = deepcopy(self)
        temp.value = temp.value * type(self.value)(other)
        return temp

    @dispatch(int)
    def __imul__(self, other):
        self.value = self.value * type(self.value)(other)
        return self

    @dispatch(int)
    def __truediv__(self, other):
        temp = deepcopy(self)
        temp.value = temp.value // type(self.value)(other)
        return temp

    @dispatch(int)
    def __itruediv__(self, other):
        self.value = self.value // type(self.value)(other)
        return self

    @dispatch(object)
    def __add__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        temp = deepcopy(self)
        temp.value = temp.value + type(temp.value)(other.value)
        return temp

    @dispatch(object)
    def __iadd__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        self.value = self.value + type(self.value)(other.value)
        return self

    @dispatch(object)
    def __sub__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        temp = deepcopy(self)
        temp.value = temp.value - type(temp.value)(other.value)
        return temp

    @dispatch(object)
    def __isub__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        self.value = self.value - type(self.value)(other.value)
        return self

    @dispatch(object)
    def __mul__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        temp = deepcopy(self)
        temp.value = temp.value * type(temp.value)(other.value)
        return temp

    @dispatch(object)
    def __imul__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        self.value = self.value * type(self.value)(other.value)
        return self

    @dispatch(object)
    def __truediv__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        temp = deepcopy(self)
        temp.value = temp.value // type(temp.value)(other.value)
        return temp

    @dispatch(object)
    def __itruediv__(self, other):
        if self.value.nbytes < other.value.nbytes:
            raise IncompatibleVariableSizes
        self.value = self.value // type(self.value)(other.value)
        return self

def variable_det_to_word(size, signed):
    size = {1: 'BYTE',
            2: 'WORD',
            4: 'DWORD',
            8: 'QWORD'}[size]
    if signed:
        size = "S{}".format(size)
    return size

def variable_word_to_type(word):
    word = word.upper()
    signed = False
    if word[0] == 'S':
        signed = True
        word = word[1:]

    word = {'BYTE': 'int8',
            'WORD': 'int16',
            'DWORD': 'int32',
            'QWORD': 'int64'}[word]
    if not signed:
        word = "u{}".format(word)

    return eval('np.{}'.format(word))

def variable_det_to_type(size, signed):
    word = {1: 'int8',
            2: 'int16',
            4: 'int32',
            8: 'int64'}[size]
    if not signed:
        word = "u{}".format(word)
    return eval('np.{}'.format(word))

def variable_word_to_det(word):
    word = word.upper()
    signed = False
    if word[0] == 'S':
        signed = True
        word = word[1:]

    word = {'BYTE': 1,
            'WORD': 2,
            'DWORD': 4,
            'QWORD': 8}[word]

    return (word, signed)

def variable_type_to_det(_type):
    det = str(_type)[14:].split("'")[0]
    signed = True
    if det[0] == 'u':
        signed = False
        det = det[1:]

    det = {'int8': 1,
           'int16': 2,
           'int32': 4,
           'int64': 8}[det]

    return (det, signed)

def variable_type_to_word(_type):
    word = str(_type)[14:].split("'")[0]
    signed = True
    if word[0] == 'u':
        signed = False
        word = word[1:]

    word = {'int8': 'BYTE',
           'int16': 'WORD',
           'int32': 'DWORD',
           'int64': 'QWORD'}[word]

    if signed:
        word = 'S{}'.format(word)

    return word

def variable_all(*args, **xargs):
    if (len(args) + len(xargs)) == 2:
        word = variable_det_to_word(*args, **xargs)
        _type = variable_det_to_type(*args, **xargs)
        try:
            size = xargs['size']
        except KeyError:
            size = args[0]

        try:
            signed = xargs['signed']
        except KeyError:
            signed = args[1]

        return {'word': word,
                'type': _type,
                'det': (size, bool(signed))}

    elif len(xargs) == 1:
        try:
            var = xargs['word']
        except KeyError:
            var = xargs['_type']
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
            'det': det}


