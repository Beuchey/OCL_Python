import weakref

class MyClass:

    _instances = set()

    def __init__(self, name):
        self.name = name
        self._instances.add(weakref.ref(self))

    @classmethod
    def getinstances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

a = MyClass("a")
b = MyClass("b")
c = MyClass("c")

del b

for obj in MyClass.getinstances():
    print(obj.name) # prints 'a' and 'c'
