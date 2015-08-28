from utils import *
from register import Register
from memory import Memory, Variable

class Command():

    def __init__(self, name, help=''):
        self.name = name
        self.help = help

    def __call__(self, *args, **xargs):
        self.__run__(*args, **xargs)

    def __run__(self, *args, **xargs):
    	pass


def runc(command, *args, **xargs):
    command.__run__(*args, **xargs)


class ADD(Command):

    def __init__(self):
        super(ADD, self).__init__('ADD', 'INSERT HELP')

    @dispatch(Register, int)
    def __run__(self, destination, source):
        destination += source

    @dispatch(Variable, int)
    def __run__(self, destination, source):
        destination += source


class MOV(Command):

    def __init__(self):
        super(MOV, self).__init__('MOV', 'INSERT HELP')

    def __run__(self, destination, source):
        destination.value = source


masm_commands = {
    'ADD': ADD(),
    'MOV': MOV()}
