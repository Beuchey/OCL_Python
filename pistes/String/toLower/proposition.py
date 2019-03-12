from __future__ import annotations # To be able to return the current class in class method. This import should become unnecessary in Python 4.0 to be able to di this.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..', 'oclpyth'))
from OclPyth import OclWrapper_Any

class OclWrapper_String(OclWrapper_Any):

    def toLower(self) -> OclWrapper_String:
        """Turns the wrapped string into a full lowercase version of itelf.

        Note:
            OCL functionnality -> 'toLower'

        Returns:
            An OclWrapper_Any wrapping a full lowercase version of the original wrapped object.

        >>> print(OclWrapper_String('IWIW').toLower())
        iwiw
        >>> print(OclWrapper_String('iwiw').toLower())
        iwiw
        >>> print(OclWrapper_String('IwIw').toLower())
        iwiw
        """
        return OclWrapper_String(self._wrapped.lower())







print(OclWrapper_String('Hello World!').toLower())
