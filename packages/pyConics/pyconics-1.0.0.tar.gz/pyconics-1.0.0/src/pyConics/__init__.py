#------------------------------------------------------------------
# __init__ dunder.
#
# It defines a package in Python.
#

#------------------------------------------------------------------
# read version from installed package
#
from importlib.metadata import version
__version__ = version( 'pyConics' )

#------------------------------------------------------------------
# Modules that belong to pyConics package.
#
from pyConics.origin import *
from pyConics.tolerance import *
from pyConics.point import *
from pyConics.line import *

from pyConics.plotting import *

