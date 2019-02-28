# oclAsType

The function oclAsType is basically a static cast allowing the user to check if an object is an instance of a class.

```Python
class A(object):
  def oclAsType(self, cls):
        """Statically cast self as the desired class.

        Note:
            OCL functionnality -> 'oclAsType'

        Args:
            cls (classinfo): Class to cast the object to.

        Returns:
            object: Self if the object if an instance of the Class, None otherwise.
        """
        if(isinstance(self, cls)):
            return self

class A_1(A):
  pass


class A_2(A):
  pass



a = A()
a_1 = a.oclAsType(A_1)
a_2 = a.oclAsType(A_2)

if(a_1 == None):
    print("a is not a A_1")
else:
    print("a is a A_1")

if(a_2 == None):
    print("a is not a A_2")
else:
    print("a is a A_2")

print("----------------------------------")

a = A_2()
a_1 = a.oclAsType(A_1)
a_2 = a.oclAsType(A_2)

if(a_1 == None):
    print("a is not a A_1")
else:
    print("a is a A_1")

if(a_2 == None):
    print("a is not a A_2")
else:
    print("a is a A_2")
```

This means we would have to create this kind of class to be a wrapper for all the classes we would like to invoke oclAsType on.
