# encoding=utf-8
"""Compare perl idioms to the python-way

Mostly from <https://everythingsysadmin.com/perl2python.html>
But use console.write() instead of print

# sleep:
#   from time import sleep
#   sleep(t)
"""
from Npp import *

def __template():
    """docstring here"""
    console.write("========== {}() ==========\n".format(sys._getframe().f_code.co_name))
    console.write("==========\n\n")

def py_formattedPrints():
    """Show various formatted print statements"""
    # header
    console.write("========== Formatted Prints ==========\n")

    # formatString % (tuple)        -- similar to sprintf notation
    console.write( "%s %% %s\n" % ("formatString", "(tuple)") )
        # even in 2.7 tutorial (https://docs.python.org/2/tutorial/inputoutput.html#old-string-formatting),
        # they call the %-notation "old string formatting"

    # formatString.format(tuple)
    console.write( "{}.format({})\n".format("formatString", "tuple") )
        # 3.x: see https://docs.python.org/3/library/stdtypes.html#str.format
        #      and https://docs.python.org/3/library/string.html#formatstrings
        # 2.7: see https://docs.python.org/2/library/string.html#formatstrings

    # py 3.6+: f'formatString' -- similar to formatString.format(tuple), but can include variable
        # see Formatted String Literals at <https://docs.python.org/3/reference/lexical_analysis.html#f-strings>
    # console.write( f"{varname}.format({})\n" )

    # I am going to pick the formatString.format(tuple), because it's closest to the f'' which should be the preferred choice for modern python

    #end
    console.write("==========\n\n")

def perl_stringJoin():
    """perl: join(', ', @array)
    python: ', '.join(tuple)
    """
    console.write("========== {}() ==========\n".format(sys._getframe().f_code.co_name))
    tuple = ('1', 'text', 'asdfadf')
    console.write(', '.join(tuple) + "\n")

    console.write("==========\n\n")

def py_introspectFunctionName():
    """shows how to introspect the function name

    came from the comments of https://stackoverflow.com/a/5067661/5508606
    """
    console.write("========== Introspect Function Name ==========\n")

    console.write("{:<12} {}()\n".format("sys:", sys._getframe().f_code.co_name))

    import inspect
    console.write("{:<12} {}()\n".format('inspect:', inspect.currentframe().f_code.co_name))
    console.write("==========\n\n")


def perl_fileReadlineLoop():
    """perl: while(<$fh>) { chomp; print ":\t$_<EOL>\n" }"""
    console.write("========== {}() ==========\n".format(sys._getframe().f_code.co_name))

    #console.write("for line in file(%s):\n" % __file__ )
    for line in file(__file__):
        """str.rstrip() is chomp
        str%(list) is a sprintf
        str.format(list) is a sprintf
        """
        console.write(":\t{}<EOL>\n".format(line.rstrip()) )

    # slurp to single string
    contents = file(__file__).read()
    console.write("slurp: length {} chars\n".format(len(contents)))
    # slurp to array of strings
    list_of_strings = file(__file__).readlines()
    console.write("list: length {} lines\n".format(len(list_of_strings)))

    console.write("==========\n\n")

def perl_regex():
    """perl's regular expressions are builtin

    python requires the re library

    my example would be equivalent of m/console\.(\w+)(.*)/, complete with matches
    """
    console.write("========== {}() ==========\n".format(sys._getframe().f_code.co_name))

    import re
    re_obj = re.compile(r'console\.(\w+)(.*)')
    for line in file(__file__):
        match_obj = re.search(re_obj, line)
        if match_obj:
            console.write("{:<16} >>{}<<\n".format( 'entire match:', match_obj.group(0).rstrip() ))
            console.write("\t{:<8} >>{}<<\n".format( 'grp#1:', match_obj.group(1) ))
            console.write("\t{:<8} >>{}<<\n".format( 'grp#2:', match_obj.group(2) ))

    console.write("==========\n\n")

def perl_foreachLoops():
    """perl: foreach $i (0 .. $#array) {} and similar"""
    console.write("========== {}() ==========\n".format(sys._getframe().f_code.co_name))

    # setup an array (tuple, so non-mutable) and a hash (dictionary)
    array = ('one' , 'two' , 'three')               # https://docs.python.org/3/library/stdtypes.html#lists             and #tuples
    hash = { 'ten':10, 'eleven':11}                 # https://docs.python.org/3/library/stdtypes.html#typesmapping

    # foreach my $i ( 0 .. $#array )
    for i in range(len(array)):                     # https://docs.python.org/3/library/stdtypes.html#ranges
        """this is the only place I like that range(max) goes from 0 .. max-1"""
        console.write("i={}, element={}\n".format(i, array[i]))

    # two more range() examples, to show the rest of range
    for i in range(7,10):
        """here's where I don't like range: it maxes out at 9, not 10"""
        console.write("range(7,10) => i={}\n".format(i))

    for i in range(20,30+1,10):
        console.write("range(20,30+1,10) => i={}\n".format(i))

    # foreach my $element ( @array )
    for element in array:
        """I actually like the python way of figuring out which index a given element is from: notation"""
        console.write("element={}, index=>{}\n".format(element, array.index(element)))

    # foreach my $v ( values %hash )
    for v in hash.values():
        console.write("value={}\n".format(v))

    # while( my ($k,$v) = each %hash )
    for k,v in hash.items():
        console.write("key={}, value={}\n".format(k, v))    # hash.index(v) does not work: >>AttributeError: 'dict' object has no attribute 'index'<<

    console.write("==========\n\n")

def perl_subroutine_args():
    """ perl sub { my(...) = @_ } """
    console.write("subroutine arguments\n")

    # sub { my ($positional, $argument) = @_ }
    def py_positional(positional, argument):
        console.write("py_positional({},{}) called\n".format(positional, argument))
    py_positional('one', 'two')

    # sub { my ($positional, $argument) = @_; $argument //= 'default' }
    def py_positional_default(positional, argument='default'):
        console.write("py_positional_default({},{}) called\n".format(positional, argument))
    py_positional_default('one')
    py_positional_default('one', 'override')

    # sub { my (@args) = @_; }
    #   also note that `[fn(x) for x in args]` is pythonesque version of perl's `fn($_) for @args`
    def py_list(*args):
        console.write("py_list({}) called\n".format(','.join([str(x) for x in args])))
    py_list('one')
    py_list(1,'mixed',3)
    py_list() # having no argument works as well

    # sub { my (%h) = @_; }
    def py_hash(**kwargs):
        ###while you can k,v in {some:'dict'}, that doesn't work in kwargs, apparently, so use k in kwargs instead, \
        ###either
        console.write("py_hash({}):\n".format(','.join(["{}=>{}".format(k,kwargs[k]) for k in kwargs])))
        ### or
        #console.write("py_hash(...):\n")
        #for k in kwargs:
        #    console.write("\t{} => {}\n".format(k,kwargs[k]))
        ### either works
    py_hash(key='value', another=None)

    console.write("==========\n\n")


if __name__ == '__main__':
    console.clear()
    console.show()

    #py_formattedPrints()
    #py_introspectFunctionName()
    #perl_fileReadlineLoop()
    #perl_regex()
    #perl_stringJoin()
    #perl_foreachLoops()
    perl_subroutine_args()
