from __future__ import annotations # To be able to return the current class in class method. This import should become unnecessary in Python 4.0 to be able to di this.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..', 'oclpyth'))
from OclPyth import OclWrapper_Any

class OclWrapper_String(OclWrapper_Any):

    def toInteger(self) -> OclWrapper_Any:
        """Parses a String into an Integer, if possible.

        Note:
            OCL functionnality -> 'toInteger'

        Returns:
            The Integer value of the wrapped object.

        >>> print(OclWrapper_String('3').toInteger())
        3
        >>> print(OclWrapper_String(OclWrapper_String('3')).toInteger())
        3
        """
        return OclWrapper_Any(int(self._wrapped))







print(OclWrapper_String('3').toInteger())
print(OclWrapper_String(OclWrapper_String('3')).toInteger())
