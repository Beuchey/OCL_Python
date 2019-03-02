class A(object):
    def oclAsType(self, cls):
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
