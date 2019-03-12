from __future__ import annotations # To be able to return the current class in class method. This import should become unnecessary in Python 4.0 to be able to di this.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..', 'oclpyth'))
from OclPyth import OclWrapper_Any

class OclWrapper_String(OclWrapper_Any):

    def toLower(self) -> OclWrapper_String:
        """Concatenates the other object (eventually already wrapped) to the wrapped string.

        Note:
            OCL functionnality -> 'concat'

        Args:
            otherObject (object): The other object to concatenate to the wrapped object.

        Returns:
            An OclWrapper_String wrapping the original wrapped object concatenated with the other object (eventually already wrapped).

        >>> print(OclWrapper_String('WWWW').toLower())
        wwww
        >>> print(OclWrapper_String('wwww').toLower())
        wwww
        >>> print(OclWrapper_String('Wwww').toLower())
        wwww
        """
        return OclWrapper_String(self._wrapped.lower())







print(OclWrapper_String('Hello World!').toLower())
