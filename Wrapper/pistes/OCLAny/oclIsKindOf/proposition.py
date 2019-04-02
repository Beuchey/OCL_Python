class A(object):
  def oclIsKindOf(self, aclass: str) -> bool:
        """Checks if the object is an instance of the Class. Just an alias for isinstance(), actually.

        Note:
            OCL functionnality -> 'oclIsKindOf'

        Args:
            cls (str): Class to check of the object is an instance of.

        Returns:
            True if the object is an instance of the class, False otherwise.

        >>> OclWrapper(True).oclIsKindOf(OclWrapper)
        True
        >>> OclWrapper(True).oclIsKindOf(bool)
        False
        """
        return isinstance(self, aclass)

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
