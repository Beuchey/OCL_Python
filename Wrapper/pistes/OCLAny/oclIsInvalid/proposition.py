class Wrapper(object):

    def __init__(self, awrapped : object):
        self.wrapped = awrapped

    def oclIsUndefined(self) -> bool:
        """Checks if the wrapped object is undefined, aka is None.

        Note:
            OCL functionnality -> 'oclIsUndefined'

        Returns:
            True if the wrapped object is undefined, aka is None, Fale otherwise.

        >>> OclWrapper(True).oclIsUndefined()
        False
        >>> OclWrapper(None).oclIsUndefined()
        True
        """
        return self.wrapped is None



a = Wrapper("2")
b = Wrapper(None)

print(a.oclIsUndefined())
print(b.oclIsUndefined())
