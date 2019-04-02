from __future__ import annotations # To be able to return the current class in class method. This import should become unnecessary in Python 4.0 to be able to di this.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..', 'oclpyth'))
from OclPyth import OclWrapper_Any

class OclWrapper_String(OclWrapper_Any):

    def size(self) -> OclWrapper_Any:
        """Returns the size, aka le length, of the wrapped object.

        Note:
            OCL functionnality -> 'size'

        Returns:
            The size, aka le length, of the wrapped object.

        >>> OclWrapper_String('Hello World!')
        12
        """
        return OclWrapper_Any(len(self._wrapped))







print(OclWrapper_String('Hello World!').size())
print(OclWrapper_String(OclWrapper_Any('Hello World!')).size())
