# substring

In OCL, indexes like in Strings begin at 1, not 0, and OCL's substring includes the end index in the result.

```Python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..', 'result'))
import OclPyth

class OclWrapper_String(OclPyth.OclWrapper):

    def substring(self, start: int, end: int) -> OclWrapper_String:
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
        """
        return OclWrapper_String(self._wrapped[start-1:end])








print(OclWrapper_String('test').substring(1,1))
print(OclWrapper_String(OclWrapper_String('test')).substring(2,4))
```
