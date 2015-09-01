#!/usr/bin/env python3
from nose.tools import *
from nose import run
import sys
import numpy as np
from register import Register
from memory import Memory, Variable
from utils import *
from stack import Stack



def test_register_value():
    eax = Register(name='eax', use='', size=32)
    assert eax.value == 0

    # Assigning new value
    eax(5)
    assert eax() == 5
    assert (eax.mem == [0, 0, 0, 5]).all()

    # Addition
    assert (eax + 5)() == 10

    # Inplace Addition
    eax += 6
    assert eax() == 11


def test_register_sub():
    eax = Register(name='eax', use='', size=32)
    eax(11)

    # Subregister
    _, ax = eax.make_subregisters('_', 'ax')
    ah, al = ax.make_subregisters('ah', 'ax')

    # memory distribution
    assert (al.mem == [11]).all()
    assert (ah.mem == [0]).all()
    assert (ax.mem == [0, 11]).all()

    ax += 255
    assert eax() == 266
    assert ax() == 266
    assert (ax.mem == [1, 10]).all()
    assert (al.mem == [10]).all()
    assert (ah.mem == [1]).all()

@raises(IncompatibleVariableSizes)
def test_register_other_types():
    eax = Register(name='eax', use='', size=32)
    _, ax = eax.make_subregisters('_', 'ax')
    ah, al = ax.make_subregisters('ah', 'ax')
    eax(15)

    var = Variable(50, 'var', 0, 4, True, True)
    assert (eax + var)() == 65

    numpy_type = np.int8(15)
    assert (eax + numpy_type)() == 30

    ax + var



if __name__ == '__main__':
    run()







