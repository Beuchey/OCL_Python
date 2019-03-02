# oclIsTypeOf

The function oclIsKindOf in OCL is has almost the same purpose than the function isinstance in Python, but it checks if the type of the object is EXACTLY the one desired, and so returns False also if the object is a generalization or specialization of the desired class.
To accomplish this, we can test if the type of the object IS the one desired.

```Python
class A(object):
  def oclIsTypeOf(self, aclass: str) -> bool:
        """Checks if the object is exactly an instance of the Class. Exactly means that it will return False even if the object is a generalization or specialization of the desired class.

        Note:
            OCL functionnality -> 'oclIsTypeOf'

        Args:
            cls (str): Class to check of the object has the type.

        Returns:
            True if the type of the object is exactly the given class, False otherwise.

        >>> OclWrapper(True).oclIsTypeOf(OclWrapper)
        True
        >>> OclWrapper(True).oclIsTypeOf(bool)
        False
        """
        return type(self) is aclass

class A_1(A):
  pass

class A_2(A):
  pass

class B(object):
  pass



a = A()
a_1 = A_1()
a_2 = A_2()

print(a.oclIsTypeOf(A))
print(a.oclIsTypeOf(A_1))
print(a.oclIsTypeOf(B))
print(a_1.oclIsTypeOf(A))
print(a_1.oclIsTypeOf(A_1))
print(a_1.oclIsTypeOf(B))
print(a_2.oclIsTypeOf(A))
print(a_2.oclIsTypeOf(A_1))
print(a_2.oclIsTypeOf(B))
```

This means we would have to create this kind of class to be a wrapper for all the classes we would like to invoke oclIsKindOf on.
