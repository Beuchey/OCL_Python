from __future__ import annotations # To be able to return the current class in class method. This import should become unnecessary in Python 4.0 to be able to di this.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..', 'oclpyth'))
from OclPyth import OclWrapper_Any

class OclWrapper_String(OclWrapper_Any):

    def concat(self, otherObject: object) -> OclWrapper_String:
        """Concatenates the other object (eventually already wrapped) to the wrapped string.

        Note:
            OCL functionnality -> 'concat'

        Args:
            otherObject (object): The other object to concatenate to the wrapped object.

        Returns:
            An OclWrapper_String wrapping the original wrapped object concatenated with the other object (eventually already wrapped).

        >>> print(OclWrapper_String('Hello World!').concat(' I am a string.'))
        Hello World! I am a string.
        >>> print(OclWrapper_String('Hello World!').concat(OclWrapper_String(' I am another string.')))
        Hello World! I am another string.
        """
        return OclWrapper_String(self._wrapped + otherObject)






astr = OclWrapper_String('Hello World!')
print(astr.concat(' I\'m a string.'))
print(astr.concat(OclWrapper_String(' I\'m a another string.')))