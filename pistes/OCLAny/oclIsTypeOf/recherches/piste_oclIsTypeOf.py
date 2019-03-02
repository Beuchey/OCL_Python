class A(object):
    def oclIsTypeOf(self, cls):
        return type(self) is cls

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
