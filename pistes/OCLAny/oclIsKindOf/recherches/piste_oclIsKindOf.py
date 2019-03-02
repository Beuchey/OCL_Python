class A(object):
    def oclIsKindOf(self, cls):
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
