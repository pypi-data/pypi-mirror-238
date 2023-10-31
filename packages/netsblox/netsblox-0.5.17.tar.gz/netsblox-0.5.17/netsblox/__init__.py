'''
A python interface for accessing NetsBlox services
'''

from .editor import * # we import editor into global scope
from . import dev     # users can access dev explicitly if they want
from . import turtle
from . import snap
from . import rooms

from .common import get_location, get_error, nothrow

__version__ = '0.5.16'
__author__ = 'Devin Jean'
__credits__ = 'Institute for Software Integrated Systems, Vanderbilt University'
