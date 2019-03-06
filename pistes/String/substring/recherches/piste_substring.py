from __future__ import annotations # To be able to return the current class in class method. This import should become unnecessary in Python 4.0 to be able to di this.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..', 'result'))
import OclPyth

class OclWrapper_String(OclPyth.OclWrapper):

    def substring(self, start: int, end: int) -> OclWrapper:
        """Slices the _wrapped object from start to end.

        Note:
            In OCL, indexes like in Strings begin at 1, not 0, and OCL's substring includes the end index in the result.

            OCL functionnality -> 'substring'

        Args:
            start (integer): The first element index to include (starting at 1)
            end (integer): The last element index to include (starting at 1)

        Returns:
            The result of the slicing from start to end on the wrapped object.

        >>> print(OclWrapper_String('test').substring(1,1))
        t
        >>> print(OclWrapper_String(OclWrapper_String('test')).substring(2,4))
        est
        >>> s = OclWrapper_String('test')
        >>> print(s.substring(1,s.size()))
        test
        """
        return OclWrapper(self._wrapped[start-1:end])

s = OclWrapper_String('test')
print(s.substring(1,s.size()))
