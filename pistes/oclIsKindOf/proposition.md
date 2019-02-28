# oclIsKindOf

The function oclIsKindOf in OCL is has the same purpose than the function isinstance in Python.

```Python
class A(object):
  def oclIsKindOf(self, cls: str) -> bool:
        """Checks if the object is an instance of the Class. Just an alias for isinstance(), actually.

        Note:
            OCL functionnality -> 'oclIsKindOf'

        Args:
            cls (classinfo): Class to check of the object is an instance of.

        Returns:
            True if the object is an instance of the class, False otherwise.

        >>> OclWrapper(True).oclIsKindOf(OclWrapper)
        True
        >>> OclWrapper(True).oclIsKindOf(bool)
        False
        """
        return isinstance(self, cls)

class A_1(A):
  pass

class A_2(A):
  pass

class B(object):
  pass



a = A()
a_1 = A_1()
a_2 = A_2()

print(a.oclIsKindOf(A))
print(a.oclIsKindOf(A_1))
print(a.oclIsKindOf(B))
print(a_1.oclIsKindOf(A))
print(a_1.oclIsKindOf(A_1))
print(a_1.oclIsKindOf(B))
print(a_2.oclIsKindOf(A))
print(a_2.oclIsKindOf(A_1))
print(a_2.oclIsKindOf(B))
```

This means we would have to create this kind of class to be a wrapper for all the classes we would like to invoke oclIsKindOf on.
