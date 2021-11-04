# encoding=utf-8
"""Quick example of a class with setters and getters...

Similar to FFFFF-Perl2Python-Idioms.py, should be in my normal python development repo, but since I need to develop in a python.exe-less environment...0
"""
from Npp import *


class Parrot(object):
    """example from https://docs.python.org/2/library/functions.html?highlight=property#property"""
    def __init__(self):
        self._voltage = 100000

    @property
    def voltage(self):
        """Get the current voltage."""
        return self._voltage

class C(object):
    """example from https://docs.python.org/2/library/functions.html?highlight=property#property"""
    def __init__(self):
        self._x = None

    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter
    def x(self, value):
        """use as obj.x = value; provides encapsulation by allowing for error checking"""
        console.write("DEBUG | obj.x:setter({}): perform error checking\n".format(value))
        self._x = value

    @x.deleter
    def x(self):
        del self._x

def main():
    """this is the function's doc string"""
    console.show()
    console.clear()

    # using the examples from https://docs.python.org/2/library/functions.html?highlight=property#property
    p = Parrot()
    console.write("repr(p) = {}\n".format(repr(p)))
    v = p.voltage
    console.write("Parrot#p.voltage = {}\n".format(v))

    o = C()
    console.write("repr(o) = {}\n".format(repr(o)))
    console.write("o._x = {}\n".format(o._x))
    console.write("o.x = {}\n".format(o.x))
    o.x = "Something new"                       # using the setter here...
        # https://www.python-course.eu/python3_properties.php showed me that you actually use the setter by putting it to the left of the equals...
        # it provides encapsulation not by making it look like a function call (ie, the o.x(value) I thought it was going to be), but by
        #   providing opportuntity for error handling, etc.  I simulated this by the "DEBUG | obj.x:setter({})" print, above
    console.write("AFTER SETTER: o.x = {}\n".format(o.x))
    del o.x
    ex = "xxx"
    try:
        #raise NotImplementedError('This hasn\'t been written yet')
        ex = o.x
    except AttributeError:
        ex = "<o.x was deleted>"
    except:
        import sys
        ex = "\t>> {}\t>> {}\t>> {}\n".format(sys.exc_type, sys.exc_value, sys.exc_traceback)
        console.write("EXCEPT: o.x = {}\n".format(ex))
        raise

    console.write("AFTER DELETER: o.x = {}\n".format(ex))

if __name__ == '__main__': main()