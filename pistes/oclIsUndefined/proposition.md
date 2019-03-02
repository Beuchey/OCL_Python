# oclIsUndefined

Use a wrapper with "is None".

```Python
class Wrapper(object):

    def __init__(self, awrapped : object):
        self.wrapped = awrapped

    def oclIsInvalid(self) -> bool:
        """Checks if the wrapped object is invalid, aka is None.

        Note:
            OCL functionnality -> 'oclIsInvalid'

        Returns:
            True if the wrapped object is invalid, aka is None, Fale otherwise.

        >>> OclWrapper(True).oclIsInvalid()
        False
        >>> OclWrapper(None).oclIsInvalid()
        True
        """
        return self.wrapped is None



a = Wrapper("2")
b = Wrapper(None)

print(a.oclIsInvalid())
print(b.oclIsInvalid())
```
