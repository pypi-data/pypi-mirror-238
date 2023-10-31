
__version__ = '1.2.6'

import sys
print("PATH: %s" % (sys.path, ))
try:
    from fibers._cfibers import *
except ImportError:
    from fibers._pyfibers import *

