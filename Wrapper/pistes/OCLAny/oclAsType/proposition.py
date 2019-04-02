class A(object):
  def oclAsType(self, aclass: str) -> object:
        """Statically cast self as the desired class.

        Note:
            OCL functionnality -> 'oclAsType'

        Args:
            cls (str): Class to cast the object to.

        Returns:
            object: Self if the object if an instance of the Class, None otherwise.

        >>> type(OclWrapper(True).oclAsType(OclWrapper)).__name__
        'OclWrapper'
        >>> type(OclWrapper(True).oclAsType(bool)).__name__
        'NoneType'
        """
        if(isinstance(self, aclass)):
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
