from __future__ import annotations # To be able to return the current class in class method. This import should become unnecessary in Python 4.0 to be able to di this.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..', 'oclpyth'))
from OclPyth import OclWrapper_Any

class OclWrapper_String(OclWrapper_Any):

    def toUpper(self) -> OclWrapper_String:
        """Turns the wrapped string into a full uppercase version of itelf.

        Note:
            OCL functionnality -> 'toUpper'

        Returns:
            An OclWrapper_Any wrapping a full uppercase version of the original wrapped object.

        >>> print(OclWrapper_String('IWIW').toUpper())
        IWIW
        >>> print(OclWrapper_String('iwiw').toUpper())
        IWIW
        >>> print(OclWrapper_String('IwIw').toUpper())
        IWIW
        """
        return OclWrapper_String(self._wrapped.upper())







print(OclWrapper_String('Hello World!').toUpper())
