"""Python interface to ICAT and IDS

This package provides a collection of modules for writing Python
programs that access an `ICAT`_ service using the SOAP interface.  It
is based on Suds and extends it with ICAT specific features.

.. _ICAT: https://icatproject.org/
"""

__version__ = "1.2.0"

#
# Default import
#

from icat.client import *
from icat.exception import *

