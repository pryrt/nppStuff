# encoding=utf-8
"""exploring enumerated classes... trying to get it to behave like Npp.ENUMs

other notes go here
"""
from Npp import editor,notepad,console

class BaseEnum():
    """BaseEnum:
        In string context, return a string.
        In numeric context, return a number.
    """
    def __init__(self, string, number):
        self._number = number
        self._string = string

    def __repr__(self):
        return "{}.{}".format(self.__class__.__name__, self._string)

    # https://docs.python.org/2.7/reference/datamodel.html#emulating-numeric-types
    def __int__(self):          return self._number
    def __add__(self, other):   return int(self) + other
    def __radd__(self, other):  return other + int(self)
    def __sub__(self, other):   return int(self) - other
    def __rsub__(self, other):  return other - int(self)
    # to make it a truly useful enum, I would have to define all the other integer-compatible math functions...

class ExampleEnum(BaseEnum):
    NONE = ExampleEnum("NONE", 0)
    CHAR = ExampleEnum("CHAR", 1)
    LINE = ExampleEnum("LINE", 2)

if __name__ == '__main__':
    # experiment with them:
    console.write("{}\n".format(ExampleEnum.CHAR))
    console.write("{}\n".format(int(ExampleEnum.CHAR)))
    console.write("{}\n".format(ExampleEnum.NONE+2.718))
    console.write("{}\n".format(ExampleEnum.NONE-2.718))
    console.write("{}\n".format(1.14+ExampleEnum.LINE))
    console.write("{}\n".format(1.14-ExampleEnum.LINE))
