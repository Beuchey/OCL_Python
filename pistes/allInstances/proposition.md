# allInstances

Python does not keep track of all instances of a class (or of a built-in type), so we would have to implement it ourselves. In order to ccomplish this, we can store a weak reference to each instance in class attribute. Here’s an example:

```Python
import weakref

class MyClass:

    _instances = set()

    def __init__(self, name):
        self.name = name
        self._instances.add(weakref.ref(self))

    @classmethod
    def allInstances(cls):
        """Allows to get, at any instant, a set of all the object of the calling class.

        Note:
            Iterates through the recorded instances of the general OCLWrapper class
            and if the objects are instances of the calling classinfo
            (eventually corresponding to a specialization of the general OCLWrapper class),
            yields them.
            Cleans up the references onto None objects before returning.

            OCL functionnality -> 'allInstances'

        Args:
            cls (classinfo): Class of the desired instances.

        Returns:
            set: Set of the instanced object of this class.
        """
        dead = set() # to remember the deads (T.T)
        for ref in cls._instances: # for every recorded instance of this general class
            obj = ref()
            if obj is None: # if the object is dead, remember it
                dead.add(ref)
            else:
                if isinstance(obj, cls): # if still alive and is an instance of this eventually specialized class, yield it
                    yield obj
        cls._instances -= dead # remove the deads from the set of instances

a = MyClass("a")
b = MyClass("b")
c = MyClass("c")

del b

for obj in MyClass.allInstances():
    print(obj.name) # prints 'a' and 'c'
```

This means we would have to create this kind of class to be a wrapper for all the classes we would like to keep track this way.
