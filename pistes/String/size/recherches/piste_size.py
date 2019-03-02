import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..', 'result'))
import OclPyth

class OclWrapper_String(OclPyth.OclWrapper):

    def size(self) -> int:
        """Returns the size, aka le length, of the wrapped object.

        Note:
            OCL functionnality -> 'size'

        Returns:
            The size, aka le length, of the wrapped object.

        >>> OclWrapper_String('Hello World!')
        12
        """
        return len(self._wrapped)







print(OclWrapper_String('Hello World!').size())
print(OclWrapper_String(OclPyth.OclWrapper('Hello World!')).size())
