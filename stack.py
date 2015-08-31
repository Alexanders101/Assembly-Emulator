from utils import *

class NoMoreObjectsInStack(Exception):
    pass
class StackFull(Exception):
    pass

class Stack(Component):
    def __init__(self, size):
        # super(Stack, self).__init__('Stack')
        Component.__init__(self, 'Stack')
        self.stack = np.zeros((size,), dtype=object)
        self.pointer = size - 1

    @property
    def value(self):
        return self.pop()

    
    def push(self, value):
        if self.pointer < 0:
            raise StackFull()
        self.stack[self.pointer] = value
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
    def __call__(self, value=None):
        if value is not None:
            self.push(value)
        else:
            return self.pop()
    def __repr__(self):
        return "{}, {}".format(self.pointer, self.stack)
    def __str__(self):
        return ("Currently {} items on the stack\nFive most recent "
                "items:\n{}".format(len(self.stack) - self.pointer - 1, 
                                    self.stack[self.pointer+1:self.pointer+6]))

if __name__ == "__main__":
    stack = Stack(50)
    print(repr(stack))
