"""
A convenient way to print the contents of a class. 

"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import numpy
import time

# import PythonTools.Debug as DEBUG

##############
# CLASSTOOLS #
##############

class ClassTools(object):
    """
    A way to print the whole class in one go. It prints the key and the value. Adapted from 'Learning Python', 4th edition, by Mark Lutz.
    
    The printError, printWarning and verbose are my own idea, no need to blame the book there.
    """

    def gatherAttrs(self):
        attrs=[]
        for key in sorted(self.__dict__):
            attrs.append("\t%20s  =  %s\n" % (format_key(key), format_print(getattr(self, key))))
        return " ".join(attrs)

    def __str__(self):
        return "[%s:\n %s]" % (self.__class__.__name__, self.gatherAttrs())

#     def printError(self, string, location = []):
#         DEBUG.printError(string, location)
#  
#     def printWarning(self, string, location = []):
#         DEBUG.printWarning(string, location)
#             
#     def verbose(self, string, flag_verbose):
#         DEBUG.verbose(string, flag_verbose)




       
def format_print(var):
    """
    format_print is a helper function for the gatherAttrs function. 
    There are a few situations:
        1) var is not a list or an ndarray, it will print the value. This include tuples
        2) var is an ndarray, the shape will be printed
        3) var is a time. It will return a readable string with the time.
        3) the var is a list, it will do recursion to print either 1 or 2
    Examples:
        42          => 42
        "car"       => "car"
        [1,2]       => [1,2]
        ndarray     => shape
        [1,ndarray] => [1, shape]
    """
    # list
    if type(var) == list:
        typ = list(range(len(var)))
        for i in range(0, len(var)):
            typ[i] = (format_print(var[i]))
        return typ
    # ndarray
    # memmap is when the array is imported a file, but not actually read until it is used (saves a lot of time for large data sets). 
    elif type(var) == numpy.ndarray or type(var) == numpy.core.memmap:
        a = numpy.shape(var)
        if len(a) == 1: 
            return str(a[0]) + " x 1"
        else:
            s = "{a}".format(a = a[0])
            a = a[1:]
            for _a in a:
                s = "{s} x {a}".format(s = s, a = _a)
            return s

    # time
    elif type(var) == time.struct_time: 
        var = time.strftime("%a, %d %b %Y %H:%M:%S", var)
        return var
    elif type(var) == float:
        return round(var, 2)
    elif type(var) == numpy.float64:
        return round(var, 2)
    # the rest
    else:
        return var



def format_key(key):
    """
    Strips keys from _. These keys are semi-protected and should be run through the getter and setter methods.
    """
    if key[0] == "_":
        key = key[1:]

    return key









