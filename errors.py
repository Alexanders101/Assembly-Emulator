#!/usr/bin/env python3
# Memory
class VariableNotInitialized(Exception):
    pass


class VariableNotDefined(Exception):
    pass


class VariableAlreadyDefined(Exception):
    pass

# Variable Sizes

class InvalidSize(Exception):
    pass


class IncompatibleVariableSizes(Exception):
    pass

# Stack
class NoMoreObjectsInStack(Exception):
    pass


class StackFull(Exception):
    pass

