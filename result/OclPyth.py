# -*- coding: utf-8 -*-

import weakref

class OclWrapper(object):
    """ A wrapper for any other objects to which we need to add functionnalities in order to match Ocl's """

    __instances = set()
    """set: Set of all instances of this classinfo

        Note:
            OCL functionnality -> 'allInstances'
    """

    def __init__(self, awrapped : object):
        """__init__ method.

        Args:
            awrapped (object): The target object of this wrapper.
        """
        self.__instances.add(weakref.ref(self)) # Keeps track of all the instances of this classinfo (OCL functionnality -> 'allInstances')
        self.__wrapped = awrapped
        """object: The wrapped object."""

    def __getattr__(self, attName: str) -> object:
        """Tries to get an attribute from the wrapped object only.

        Note:
            Method automatically invoked by __getattribute__ when it doesn't find the attribute inside the current class.

            Base wrap mechanism functionnality.

        Args:
            attName (str): Name of the desired attribute.

        Returns:
            object: The desired attribute, from the wrapped.

        Raises:
            TypeError: If the wrapped doesn't support the attribute reference
        """
        return object.__getattribute__(self.__wrapped, attName)

    def __getattribute__(self, attName: str) -> object:
        """Tries to get an object from the wrapper object, and if fails, tries to get it from the wrapped object instead.

        Note:
            Method automatically invoked with '.' operator.
            Tries to simply return the attribute in the current wrapper class
            (by invoking the simpler implementation of this getter that is defined in the super-class (object))
            and if this fails (because the attribute is not defined in this class)
            that implementation will fail, so our will fail too, so it will
            automatically invoke __getattr__ instead, from this wrapper class,
            which implements an invokation of the simpler __getattribute__ from the super-class (object)
            but this time called on the wrapped object, in order to redo all the processus on this wrapped object instead
            and eventually find the attribute we are lokking for in it.
            If, finally, the attribute is not defined in the wrapper, all this will finally fail.

            Base wrap mechanism functionnality.

        Args:
            attName (str): Name of the desired attribute.

        Returns:
            object: The desired attribute, from the wrapper if an attribute with this name exists in it, or from the wrapped if not.

        Raises:
            TypeError: If neither the wrapped or the wrapper support the attribute.
        """
        return object.__getattribute__(self, attName)

    @classmethod
    def allInstances(cls: str) -> set:
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
        for ref in cls.__instances: # for every recorded instance of this general class
            obj = ref()
            if obj is None: # if the object is dead, remember it
                dead.add(ref)
            else:
                if isinstance(obj, cls): # if still alive and is an instance of this eventually specialized class, yield it
                    yield obj
        cls.__instances -= dead # remove the deads from the set of instances

    def oclAsType(self, cls: str) -> object:
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

    def oclIsKindOf(self, cls: str) -> bool:
        """Checks if the object is an instance of the Class. Just an alias for isinstance(), actually.

        Note:
            OCL functionnality -> 'oclIsKindOf'

        Args:
            cls (classinfo): Class to check of the object is an instance of.

        Returns:
            True if the object is an instance of the class, False otherwise.
        """
        return isinstance(self, cls)

    def oclIsTypeOf(self, cls: str) -> bool:
        """Checks if the object is exactly an instance of the Class. Exactly means that it will return False even if the object is a generalization or specialization of the desired class.

        Note:
            OCL functionnality -> 'oclIsTypeOf'

        Args:
            cls (classinfo): Class to check of the object has the type.

        Returns:
            True if the type of the object is exactly the given class, False otherwise.
        """
        return type(self) is cls

    def oclIsInvalid(self) -> bool:
        """Checks if the wrapped object is invalid, aka is None.

        Note:
            OCL functionnality -> 'oclIsInvalid'

        Returns:
            True if the wrapped object is invalid, aka is None, Fale otherwise.
        """
        return self.__wrapped is None





class OclWrapper_Extended(OclWrapper):
    """ Example of OclWrapper with additionnal functionnality """

    def sayHello(self):
        print("Hello from ", self.__wrapped, "!")








# Ocl functionnality -> allInstances
a = OclWrapper("a")
b = OclWrapper("b")
c = OclWrapper(1)
del b
for obj in OclWrapper.allInstances():
    print(obj)
print("----------------------------------------------")
d = OclWrapper_Extended("d")
e = OclWrapper_Extended("e")
f = OclWrapper_Extended(2)
del e
for obj in OclWrapper.allInstances():
    print(obj)
print("----------------------------------------------")
for obj in OclWrapper_Extended.allInstances():
    print(obj)
    obj.sayHello()
'''
'''
# Ocl functionnality -> oclAsType
a = OclWrapper("a")
a_e = a.oclAsType(OclWrapper_Extended)
if(a_e == None):
    print("a is not a OclWrapper_Extended")
else:
    print("a is a OclWrapper_Extended")
print("----------------------------------")
a = OclWrapper_Extended("a")
a_e = a.oclAsType(OclWrapper_Extended)
if(a_e == None):
    print("a is not a OclWrapper_Extended")
else:
    print("a is a OclWrapper_Extended")
a.oclAsType(OclWrapper_Extended).sayHello()
'''
'''
# Ocl functionnality -> oclIsKindOf
a = OclWrapper("a")
b = OclWrapper_Extended(1)
print(a.oclIsKindOf(OclWrapper))
print(a.oclIsKindOf(OclWrapper_Extended))
print(b.oclIsKindOf(OclWrapper))
print(b.oclIsKindOf(OclWrapper_Extended))
'''
'''
# Ocl functionnality -> oclIsTypeOf
a = OclWrapper("a")
b = OclWrapper_Extended(1)
print(a.oclIsTypeOf(OclWrapper))
print(a.oclIsTypeOf(OclWrapper_Extended))
print(b.oclIsTypeOf(OclWrapper))
print(b.oclIsTypeOf(OclWrapper_Extended))
'''
'''
# Ocl functionnality -> oclIsInvalid
a = OclWrapper("a")
b = OclWrapper_Extended(None)
print(a.oclIsInvalid())
print(b.oclIsInvalid())
'''
