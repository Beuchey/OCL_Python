# toInteger

Simply calls int() builtin.

```Python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..', 'result'))
import OclPyth

class OclWrapper_String(OclPyth.OclWrapper):

    def toInteger(self) -> int:
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
        return int(self._wrapped)







print(OclWrapper_String('3').toInteger())
print(OclWrapper_String(OclWrapper_String('3')).toInteger())
```
