from utils import *

class NoMoreObjectsInStack(Exception):
    pass
class StackFull(Exception):
    pass

class Stack(Component):
    def __init__(self, size):
        # super(Stack, self).__init__('Stack')
        Component.__init__(self, 'Stack')
        self.stack = np.zeros((size,), dtype=np.int32)
        self.pointer = size - 1

    def push(self, value):
        if self.pointer < 0:
            raise StackFull()
        self.stack[self.pointer] = np.int32(value)
        self.pointer -= 1

    def pop(self):
        self.pointer += 1
        try:
            value = self.stack[self.pointer]
        except IndexError:
            self.pointer -= 1
            raise NoMoreObjectsInStack()

        self.stack[self.pointer] = np.int32(0)
        return value

if __name__ == "__main__":
    stack = Stack(5)
    stack.push(12)
    hex(stack.pop())
    stack.stack
