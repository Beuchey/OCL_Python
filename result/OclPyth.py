# -*- coding: utf-8 -*-
from __future__ import annotations # To be able to return the current class in class method. This import should become unnecessary in Python 4.0 to be able to di this.
import doctest
import weakref



class OclWrapper(object):
    """ A wrapper for any other objects to which we need to add functionnalities in order to match Ocl's """

    # Class attributes

    __instances = set()
    """set: Set of all instances of this classinfo

        Note:
            OCL functionnality -> 'allInstances'
    """

    # Definition of instance attributes

    def __init__(self, awrapped : object):
        """__init__ method.

        Args:
            awrapped (object): The target object of this wrapper.
        """
        self.__instances.add(weakref.ref(self)) # Keeps track of all the instances of this classinfo (OCL functionnality -> 'allInstances')
        if(isinstance(awrapped, OclWrapper)):
            object.__setattr__(self, '_wrapped', awrapped._wrapped)
        else:
            object.__setattr__(self, '_wrapped', awrapped)
        """object: The wrapped object.
            We test if the wrapped object is already an OclWrapper, in which case we flatten it,
            so we don't end with unnecessary multiple wrapping levels.
        """

    # Basic wrapping mechanism : if the attribute is one of the wrapper, get this one, if not, look in the wrapped

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
        return object.__getattribute__(self._wrapped, attName)

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

        >>> OclWrapper(True)._wrapped
        True
        >>> OclWrapper(1)._wrapped
        1
        >>> OclWrapper('Hello')._wrapped
        'Hello'
        >>> OclWrapper((1, 2, 3))._wrapped
        (1, 2, 3)
        >>> OclWrapper([1, 2, 3])._wrapped
        [1, 2, 3]
        >>> OclWrapper({'a': 1, 'b': 2, 'c': 3})._wrapped
        {'a': 1, 'b': 2, 'c': 3}
        """
        return object.__getattribute__(self, attName)

    # Lock some attributes, avoiding simple settings et deletings

    @classmethod
    def _isLocked(self, name: str) -> bool:
        """Check if the attribute name is one of the locked ones.

        Args:
            name (str): The name of the attribute to check.

        Returns:
            True if the name is one of the locked attributes, False otherwise.

        >>> OclWrapper._isLocked('_wrapped')
        True
        >>> OclWrapper._isLocked('__instances')
        True
        >>> OclWrapper._isLocked('anyThingElse')
        False
        """
        return name=="_wrapped" or name=="__instances"

    def __setattr__(self, name: str, value: object):
        """Avoids direct setting of the _wrapped attribute.

        >>> OclWrapper(True)._wrapped = False
        Traceback (most recent call last):
        AttributeError
        """
        if (OclWrapper._isLocked(name)):
            raise AttributeError
        else:
            object.__setattr__(self, name, value)

    def __delattr__(self, name):
        """Avoids direct deleting of the _wrapped attribute.

        >>> del OclWrapper(True)._wrapped
        Traceback (most recent call last):
        AttributeError
        >>> del OclWrapper(True).__instances
        Traceback (most recent call last):
        AttributeError
        """
        if (OclWrapper._isLocked(name)):
            raise AttributeError
        else:
            object.__delattr__(self, name)

    # Basic customization

    def __repr__(self) -> str:
        """__repr__ method.

        Returns:
            The "official" string representation of the instanced object.

        >>> repr(OclWrapper(True))
        'WRAPPED : True'
        >>> repr(OclWrapper(1))
        'WRAPPED : 1'
        >>> repr(OclWrapper((1, 2, 3)))
        'WRAPPED : (1, 2, 3)'
        >>> repr(OclWrapper([1, 2, 3]))
        'WRAPPED : [1, 2, 3]'
        >>> repr(OclWrapper({'a': 1, 'b': 2, 'c': 3}))
        "WRAPPED : {'a': 1, 'b': 2, 'c': 3}"
        """
        return 'WRAPPED : ' + self._wrapped.__repr__()

    def __str__(self) -> str:
        """__str__ method.

        Note:
            Delegates the __str__ method to the wrapped object.

        Returns:
            The quick string representation of the instanced object.

        >>> print(OclWrapper(True))
        True
        >>> print(OclWrapper(1))
        1
        >>> print(OclWrapper('Hello'))
        Hello
        >>> print(OclWrapper((1, 2, 3)))
        (1, 2, 3)
        >>> print(OclWrapper([1, 2, 3]))
        [1, 2, 3]
        >>> print(OclWrapper({'a': 1, 'b': 2, 'c': 3}))
        {'a': 1, 'b': 2, 'c': 3}
        """
        return self._wrapped.__str__()

    # Boolean identity

    def __lt__(self, otherObject) -> OclWrapper:
        """__lt__ method.

        Note:
            Delegates the __lt__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to compare this one to.

        Returns:
            An OclWrapper wrapping the result of the original wrapped object compared to the other object.

        >>> print(OclWrapper(1) < 2)
        True
        >>> print(OclWrapper(1) < OclWrapper(2))
        True
        >>> print(OclWrapper(2) < 1)
        False
        >>> print(OclWrapper(2) < OclWrapper(1))
        False
        """
        return OclWrapper(self._wrapped < otherObject)

    def __le__(self, otherObject) -> OclWrapper:
        """__te__ method.

        Note:
            Delegates the __te__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to compare this one to.

        Returns:
            An OclWrapper wrapping the result of the original wrapped object compared to the other object.

        >>> print(OclWrapper(1) <= 2)
        True
        >>> print(OclWrapper(1) <= OclWrapper(2))
        True
        >>> print(OclWrapper(2) <= 1)
        False
        >>> print(OclWrapper(2) <= OclWrapper(1))
        False
        >>> print(OclWrapper(1) <= 1)
        True
        >>> print(OclWrapper(1) <= OclWrapper(1))
        True
        """
        return OclWrapper(self._wrapped <= otherObject)

    def __eq__(self, otherObject: object) -> bool:
        """__eq__ method.

        Note:
            Delegates the __eq__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to compare this one to.

        Returns:
            An OclWrapper wrapping the result of the original wrapped object compared to the other object.

        >>> print(OclWrapper(1) == 1)
        True
        >>> print(OclWrapper(1) == OclWrapper(1))
        True
        >>> print(OclWrapper(1) == 2)
        False
        >>> print(OclWrapper(1) == OclWrapper(2))
        False
        """
        return self._wrapped == otherObject

    def __hash__(self):
        """__hash__ method.

        Note:
            Delegates the __hash__ method to the parent class : object.
            This is mandatory to keep the class hashable, since the __eq__ method has been overloaded.
            Otherwise, class is delared unshashable and can't be used in hashable collections, and
            its instances can't be correctly compared to any other instances of any object.

        Returns:
            The hash value of the instanced object.

        >>> print(hash(OclWrapper(1)) == hash(OclWrapper(1)))
        True
        >>> a = OclWrapper(1)
        >>> print(hash(a) == hash(a))
        True
        >>> a = OclWrapper(1)
        >>> b = OclWrapper(1)
        >>> print(hash(a) == hash(b))
        False
        """
        return object.__hash__(self)

    def __bool__(self) -> Bool:
        """__bool__ method.

        Note:
            Delegates the __bool__ method to the wrapped object.

        Returns:
            The boolean signification of the wrapped object.

        >>> print('Yes' if OclWrapper(True) else 'No')
        Yes
        >>> print('Yes' if OclWrapper(False) else 'No')
        No
        """
        return self._wrapped.__bool__()

    def __ge__(self, otherObject) -> OclWrapper:
        """__ge__ method.

        Note:
            Delegates the __ge__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to compare this one to.

        Returns:
            An OclWrapper wrapping the result of the original wrapped object compared to the other object.

        >>> print(OclWrapper(1) >= 2)
        False
        >>> print(OclWrapper(1) >= OclWrapper(2))
        False
        >>> print(OclWrapper(2) >= 1)
        True
        >>> print(OclWrapper(2) >= OclWrapper(1))
        True
        >>> print(OclWrapper(1) >= OclWrapper(1))
        True
        >>> print(OclWrapper(1) >= 1)
        True
        """
        return OclWrapper(self._wrapped >= otherObject)

    def __gt__(self, otherObject) -> OclWrapper:
        """__gt__ method.

        Note:
            Delegates the __gt__ method to the wrapped object.

        Args:
            otherObject (object): The other object to compare this one to and creates an OclWrapper.

        Returns:
            An OclWrapper wrapping the result of the original wrapped object compared to the other object.

        >>> print(OclWrapper(1) > 2)
        False
        >>> print(OclWrapper(1) > OclWrapper(2))
        False
        >>> print(OclWrapper(2) > 1)
        True
        >>> print(OclWrapper(2) > OclWrapper(1))
        True
        """
        return OclWrapper(self._wrapped > otherObject)

    # Emulating callable objects

    def __call__(self, *args: object) -> object:
        """__call__ method.

        Note:
            Delegates the __call__ method to the wrapped object.

        Returns:
            The return value of the call to the wrapped objet with those arguments.

        >>> OclWrapper(lambda x : x + 1)(2)
        3
        >>> OclWrapper(lambda x : x + ' world!')('Hello')
        'Hello world!'
        >>> OclWrapper(lambda x : x + (3,))((1, 2))
        (1, 2, 3)
        >>> OclWrapper(lambda x : x + [3])([1, 2])
        [1, 2, 3]
        """
        return self._wrapped.__call__(*args)

    #  Emulating container types

    def __len__(self) -> int:
        """__len__ method.

        Note:
            Delegates the __len__ method to the wrapped object.

        Returns:
            The length of the wrapped objet.

        >>> len(OclWrapper('Hello'))
        5
        >>> len(OclWrapper((1, 2, 3)))
        3
        >>> len(OclWrapper([1, 2, 3, 4]))
        4
        >>> len(OclWrapper({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}))
        6
        """
        return self._wrapped.__len__()

    def __length_hint__(self) -> int:
        """__length_hint__ method.

        Note:
            Delegates the __length_hint__ method to the wrapped object.

        Returns:
            The length hint of the wrapped objet.
        """
        return self._wrapped.__length_hint__()

    def __getitem__(self, key: object) -> object:
        """__getitem__ method.

        Note:
            Delegates the __getitem__ method to the wrapped object.

        Args:
            key (object): Key of the item to get.

        Returns:
            The object returned by the wrapped object.

        >>> OclWrapper((1, 2, 3))[1]
        2
        >>> OclWrapper('Hello world!')[1]
        'e'
        >>> OclWrapper([1, 2, 3])[2]
        3
        >>> OclWrapper({'a': 1, 'b': 2, 'c': 3})['c']
        3
        """
        return self._wrapped.__getitem__(key)

    def __setitem__(self, key: object, item: object):
        """__setitem__ method.

        Note:
            Delegates the __setitem__ method to the wrapped object.

        Args:
            key (object): Key of the item to set.

        >>> a = OclWrapper([1, 2, 3])
        >>> a[1] = 'A'
        >>> print(a)
        [1, 'A', 3]
        >>> a = OclWrapper({'a': 1, 'b': 2, 'c': 3})
        >>> a['b'] = 'A'
        >>> print(a)
        {'a': 1, 'b': 'A', 'c': 3}
        """
        self._wrapped.__setitem__(key, item)

    def __delitem__(self, key: object):
        """__delitem__ method.

        Note:
            Delegates the __delitem__ method to the wrapped object.

        Args:
            key (object): Key of the item to delete.

        >>> a = OclWrapper([1, 2, 3])
        >>> del a[1]
        >>> print(a)
        [1, 3]
        >>> a = OclWrapper({'a': 1, 'b': 2, 'c': 3})
        >>> del a['b']
        >>> print(a)
        {'a': 1, 'c': 3}
        """
        return self._wrapped.__delitem__(key)

    def __missing__(self, key: object):
        """__missing__ method.

        Note:
            Delegates the __missing__ method to the wrapped object.

        Args:
            key (object): Key of the missing item.
        """
        return self._wrapped.__missing__(key)

    def __iter__(self):
        """__iter__ method.

        Note:
            Delegates the __iter__ method to the wrapped object.

        >>> next(iter(OclWrapper([2, 3, 1])))
        2
        >>> next(iter(OclWrapper((2, 3, 1))))
        2
        >>> next(iter(OclWrapper({'a':2, 'b':3, 'c':1})))
        'a'
        >>> next(iter(OclWrapper('Hello world!')))
        'H'
        """
        return self._wrapped.__iter__()

    def __next__(self):
        """__next__ method.

        Note:
            Delegates the __next__ method to the wrapped object.

        >>> it = iter(OclWrapper([2, 3, 1]))
        >>> next(it)
        2
        >>> next(it)
        3
        >>> it = iter(OclWrapper((2, 3, 1)))
        >>> next(it)
        2
        >>> next(it)
        3
        >>> it = iter(OclWrapper({'a':2, 'b':3, 'c':1}))
        >>> next(it)
        'a'
        >>> next(it)
        'b'
        >>> it = iter(OclWrapper('Hello world!'))
        >>> next(it)
        'H'
        >>> next(it)
        'e'
        """
        return self._wrapped.__next__()

    def __reversed__(self):
        """__reversed__ method.

        Note:
            Delegates the __reversed__ method to the wrapped object.

        >>> it = reversed(OclWrapper([2, 3, 1]))
        >>> next(it)
        1
        >>> next(it)
        3
        """
        return self._wrapped.__reversed__()

    def contains(self, item: object) -> bool:
        """__contains__ method.

        Note:
            Delegates the __contains__ method to the wrapped object.

        Args:
            item (object) : The object to check if it is contained by the wrapped object.

        Returns:
            True if the wrapped object contains the item, False otherwise.

        >>> OclWrapper([2, 3, 1]).contains(3)
        True
        >>> OclWrapper([2, 3, 1]).contains(4)
        False
        >>> OclWrapper((2, 3, 1)).contains(3)
        True
        >>> OclWrapper((2, 3, 1)).contains(4)
        False
        >>> OclWrapper({'a':2, 'b':3, 'c':1}).contains('b')
        True
        >>> OclWrapper({'a':2, 'b':3, 'c':1}).contains('d')
        False
        >>> OclWrapper('Hello world!').contains('o')
        True
        >>> OclWrapper('Hello world!').contains('z')
        False

        >>> OclWrapper([2, 3, 1]).__contains__(3)
        True
        >>> OclWrapper([2, 3, 1]).__contains__(4)
        False
        >>> OclWrapper((2, 3, 1)).__contains__(3)
        True
        >>> OclWrapper((2, 3, 1)).__contains__(4)
        False
        >>> OclWrapper({'a':2, 'b':3, 'c':1}).__contains__('b')
        True
        >>> OclWrapper({'a':2, 'b':3, 'c':1}).__contains__('d')
        False
        >>> OclWrapper('Hello world!').__contains__('o')
        True
        >>> OclWrapper('Hello world!').__contains__('z')
        False
        """
        return self._wrapped.__contains__(item)

    # Emulating numeric types

    def __add__(self, otherObject: object) -> OclWrapper:
        """__add__ method.

        Note:
            Delegates the __add__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to add to this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(OclWrapper(1) + 2)
        3
        >>> print(OclWrapper(1) + OclWrapper(2))
        3
        >>> print(OclWrapper('Hello') + ' world!')
        Hello world!
        >>> print(OclWrapper('Hello') + OclWrapper(' world!'))
        Hello world!
        >>> print(OclWrapper((1, 2)) + (3, 4))
        (1, 2, 3, 4)
        >>> print(OclWrapper((1, 2)) + OclWrapper((3, 4)))
        (1, 2, 3, 4)
        >>> print(OclWrapper([1, 2]) + [3, 4])
        [1, 2, 3, 4]
        >>> print(OclWrapper([1, 2]) + OclWrapper([3, 4]))
        [1, 2, 3, 4]
        """
        return OclWrapper(self._wrapped + otherObject)

    def __sub__(self, otherObject: object) -> OclWrapper:
        """__sub__ method.

        Note:
            Delegates the __sub__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to sub from this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(OclWrapper(1) - 2)
        -1
        >>> print(OclWrapper(1) - OclWrapper(2))
        -1
        """
        return OclWrapper(self._wrapped - otherObject)

    def __mul__(self, otherObject: object) -> OclWrapper:
        """__mul__ method.

        Note:
            Delegates the __mul__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to mul this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(OclWrapper(1) * 2)
        2
        >>> print(OclWrapper(1) * OclWrapper(2))
        2
        """
        return OclWrapper(self._wrapped * otherObject)

    def __matmul__(self, otherObject: object) -> OclWrapper:
        """__matmul__ method.

        Note:
            Delegates the __matmul__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to mul this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.
        """
        return OclWrapper(self._wrapped @ otherObject)

    def __truediv__(self, otherObject: object) -> OclWrapper:
        """__truediv__ method.

        Note:
            Delegates the __truediv__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to div this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(OclWrapper(1) / 2)
        0.5
        >>> print(OclWrapper(1) / OclWrapper(2))
        0.5
        """
        return OclWrapper(self._wrapped / otherObject)

    def __floordiv__(self, otherObject: object) -> OclWrapper:
        """__floordiv__ method.

        Note:
            Delegates the __floordiv__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to div this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(OclWrapper(1) // 2)
        0
        >>> print(OclWrapper(1) // OclWrapper(2))
        0
        """
        return OclWrapper(self._wrapped // otherObject)

    def __mod__(self, otherObject: object) -> OclWrapper:
        """__mod__ method.

        Note:
            Delegates the __mod__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to mod this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(OclWrapper(3) % 2)
        1
        >>> print(OclWrapper(3) % OclWrapper(2))
        1
        """
        return OclWrapper(self._wrapped % otherObject)

    def __divmod__(self, otherObject: object) -> OclWrapper:
        """__divmod__ method.

        Note:
            Delegates the __divmod__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to mod this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(divmod(OclWrapper(7), 2))
        (3, 1)
        >>> print(divmod(OclWrapper(7), OclWrapper(2)))
        (3, 1)
        """
        return OclWrapper(divmod(self._wrapped, otherObject))

    def __pow__(self, otherObject: object) -> OclWrapper:
        """__pow__ method.

        Note:
            Delegates the __pow__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to pow this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(pow(OclWrapper(2), 3))
        8
        >>> print(pow(OclWrapper(2), OclWrapper(3)))
        8
        """
        return OclWrapper(pow(self._wrapped, otherObject))

    def __lshift__(self, otherObject: object) -> OclWrapper:
        """__lshift__ method.

        Note:
            Delegates the __lshift__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to lshift this one of.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(OclWrapper(2) << 1)
        4
        >>> print(OclWrapper(2) << OclWrapper(2))
        8
        """
        return OclWrapper(self._wrapped << otherObject)

    def __rshift__(self, otherObject: object) -> OclWrapper:
        """__rshift__ method.

        Note:
            Delegates the __rshift__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to rshift this one of.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(OclWrapper(4) >> 1)
        2
        >>> print(OclWrapper(4) >> OclWrapper(2))
        1
        """
        return OclWrapper(self._wrapped >> otherObject)

    def __and__(self, otherObject: object) -> OclWrapper:
        """__and__ method.

        Note:
            Delegates the __and__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "and" with.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(OclWrapper(3) & 1)
        1
        >>> print(OclWrapper(3) & OclWrapper(1))
        1
        """
        return OclWrapper(self._wrapped & otherObject)

    def __or__(self, otherObject: object) -> OclWrapper:
        """__or__ method.

        Note:
            Delegates the __or__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "or" with.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(OclWrapper(3) | 1)
        3
        >>> print(OclWrapper(3) | OclWrapper(1))
        3
        """
        return OclWrapper(self._wrapped | otherObject)

    def __xor__(self, otherObject: object) -> OclWrapper:
        """__xor__ method.

        Note:
            Delegates the __xor__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "xor" with.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(OclWrapper(3) ^ 1)
        2
        >>> print(OclWrapper(3) ^ OclWrapper(1))
        2
        """
        return OclWrapper(self._wrapped ^ otherObject)

    def __radd__(self, otherObject) -> OclWrapper:
        """__radd__ method.

        Note:
            Delegates the __radd__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to add this one to.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(2 + OclWrapper(1))
        3
        >>> print(OclWrapper(1) + OclWrapper(2))
        3
        >>> print(sum([OclWrapper(1), OclWrapper(2)]))
        3
        >>> print('Hello' + OclWrapper(' world!'))
        Hello world!
        >>> print(OclWrapper('Hello') + OclWrapper(' world!'))
        Hello world!
        >>> print((1, 2) + OclWrapper((3, 4)))
        (1, 2, 3, 4)
        >>> print(OclWrapper((1, 2)) + OclWrapper((3, 4)))
        (1, 2, 3, 4)
        >>> print([1, 2] + OclWrapper([3, 4]))
        [1, 2, 3, 4]
        >>> print(OclWrapper([1, 2]) + OclWrapper([3, 4]))
        [1, 2, 3, 4]
        """
        return OclWrapper(otherObject + self._wrapped)

    def __rsub__(self, otherObject) -> OclWrapper:
        """__rsub__ method.

        Note:
            Delegates the __rsub__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to sub this one from.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(2 - OclWrapper(1))
        1
        >>> print(OclWrapper(2) - OclWrapper(1))
        1
        """
        return OclWrapper(otherObject - self._wrapped)

    def __rmul__(self, otherObject: object) -> OclWrapper:
        """__rmul__ method.

        Note:
            Delegates the __rmul__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to mul this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(2 * OclWrapper(1))
        2
        >>> print(OclWrapper(2) * OclWrapper(1))
        2
        """
        return OclWrapper(otherObject * self._wrapped)

    def __rmatmul__(self, otherObject: object) -> OclWrapper:
        """__rmatmul__ method.

        Note:
            Delegates the __rmatmul__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to mul this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.
        """
        return OclWrapper(otherObject @ self._wrapped)

    def __rtruediv__(self, otherObject: object) -> OclWrapper:
        """__rtruediv__ method.

        Note:
            Delegates the __rtruediv__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to div this one by.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(1 / OclWrapper(2))
        0.5
        >>> print(OclWrapper(1) / OclWrapper(2))
        0.5
        """
        return OclWrapper(otherObject / self._wrapped)

    def __rfloordiv__(self, otherObject: object) -> OclWrapper:
        """__rfloordiv__ method.

        Note:
            Delegates the __rfloordiv__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to div this one by.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(1 // OclWrapper(2))
        0
        >>> print(OclWrapper(1) // OclWrapper(2))
        0
        """
        return OclWrapper(otherObject // self._wrapped)

    def __rmod__(self, otherObject: object) -> OclWrapper:
        """__rmod__ method.

        Note:
            Delegates the __rmod__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to mod by this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(3 % OclWrapper(2))
        1
        >>> print(OclWrapper(3) % OclWrapper(2))
        1
        """
        return OclWrapper(otherObject % self._wrapped)

    def __rdivmod__(self, otherObject: object) -> OclWrapper:
        """__rdivmod__ method.

        Note:
            Delegates the __rdivmod__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to mod this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(divmod(7, OclWrapper(2)))
        (3, 1)
        >>> print(divmod(OclWrapper(7), OclWrapper(2)))
        (3, 1)
        """
        return OclWrapper(divmod(otherObject,self._wrapped))

    def __rpow__(self, otherObject: object) -> OclWrapper:
        """__rpow__ method.

        Note:
            Delegates the __rpow__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to be pow by this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(pow(2, OclWrapper(3)))
        8
        >>> print(pow(OclWrapper(2), OclWrapper(3)))
        8
        """
        return OclWrapper(pow(otherObject, self._wrapped))

    def __rlshift__(self, otherObject: object) -> OclWrapper:
        """__rlshift__ method.

        Note:
            Delegates the __rlshift__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to rlshift of this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(2 << OclWrapper(1))
        4
        >>> print(OclWrapper(2) << OclWrapper(2))
        8
        """
        return OclWrapper(otherObject << self._wrapped)

    def __rrshift__(self, otherObject: object) -> OclWrapper:
        """__rrshift__ method.

        Note:
            Delegates the __rrshift__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to rrshift of this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(4 >> OclWrapper(1))
        2
        >>> print(OclWrapper(4) >> OclWrapper(2))
        1
        """
        return OclWrapper(otherObject >> self._wrapped)

    def __rand__(self, otherObject: object) -> OclWrapper:
        """__rand__ method.

        Note:
            Delegates the __rand__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "rand" with.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(3 & OclWrapper(1))
        1
        >>> print(OclWrapper(3) & OclWrapper(1))
        1
        """
        return OclWrapper(otherObject & self._wrapped)

    def __ror__(self, otherObject: object) -> OclWrapper:
        """__ror__ method.

        Note:
            Delegates the __ror__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "ror" with.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(3 | OclWrapper(1))
        3
        >>> print(OclWrapper(3) | OclWrapper(1))
        3
        """
        return OclWrapper(otherObject | self._wrapped)

    def __rxor__(self, otherObject: object) -> OclWrapper:
        """__rxor__ method.

        Note:
            Delegates the __rxor__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "rxor" with.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(3 ^ OclWrapper(1))
        2
        >>> print(OclWrapper(3) ^ OclWrapper(1))
        2
        """
        return OclWrapper(self._wrapped ^ otherObject)

    @classmethod
    def allInstances(aclass: str) -> set:
        """Allows to get, at any instant, a set of all the object of the calling class.

        Note:
            Iterates through the recorded instances of the general OCLWrapper class
            and if the objects are instances of the calling classinfo
            (eventually corresponding to a specialization of the general OCLWrapper class),
            yields them.
            Cleans up the references onto None objects before returning.

            OCL functionnality -> 'allInstances'

        Args:
            aclass (str): class of the desired instances.

        Returns:
            set: Set of the instanced object of this class.
        """
        dead = set() # to remember the deads (T.T)
        for ref in OclWrapper.__instances: # for every recorded instance of this general class
            obj = ref()
            if obj is None: # if the object is dead, remember it
                dead.add(ref)
            else:
                if isinstance(obj, aclass): # if still alive and is an instance of this eventually specialized class, yield it
                    yield obj
        OclWrapper.__instances -= dead # remove the deads from the set of instances

    def oclAsType(self, aclass: str) -> object:
        """Statically cast self as the desired class.

        Note:
            OCL functionnality -> 'oclAsType'

        Args:
            aclass (str): class to cast the object to.

        Returns:
            object: Self if the object if an instance of the class, None otherwise.

        >>> type(OclWrapper(True).oclAsType(OclWrapper)).__name__
        'OclWrapper'
        >>> type(OclWrapper(True).oclAsType(bool)).__name__
        'NoneType'
        """
        if(isinstance(self, aclass)):
            return self

    def oclIsKindOf(self, aclass: str) -> bool:
        """Checks if the object is an instance of the class. Just an alias for isinstance(), actually.

        Note:
            OCL functionnality -> 'oclIsKindOf'

        Args:
            aclass (str): class to check of the object is an instance of.

        Returns:
            True if the object is an instance of the class, False otherwise.

        >>> OclWrapper(True).oclIsKindOf(OclWrapper)
        True
        >>> OclWrapper(True).oclIsKindOf(bool)
        False
        """
        return isinstance(self, aclass)

    def oclIsTypeOf(self, aclass: str) -> bool:
        """Checks if the object is exactly an instance of the class. Exactly means that it will return False even if the object is a generalization or specialization of the desired class.

        Note:
            OCL functionnality -> 'oclIsTypeOf'

        Args:
            aclass (str): class to check of the object has the type.

        Returns:
            True if the type of the object is exactly the given class, False otherwise.

        >>> OclWrapper(True).oclIsTypeOf(OclWrapper)
        True
        >>> OclWrapper(True).oclIsTypeOf(bool)
        False
        """
        return type(self) is aclass

    def oclIsInvalid(self) -> bool:
        """Checks if the wrapped object is invalid, aka is None.

        Note:
            OCL functionnality -> 'oclIsInvalid'

        Returns:
            True if the wrapped object is invalid, aka is None, Fale otherwise.

        >>> OclWrapper(True).oclIsInvalid()
        False
        >>> OclWrapper(None).oclIsInvalid()
        True
        """
        return self._wrapped is None

    def oclIsUndefined(self) -> bool:
        """Checks if the wrapped object is undefined, aka is None.

        Note:
            OCL functionnality -> 'oclIsUndefined'

        Returns:
            True if the wrapped object is undefined, aka is None, Fale otherwise.

        >>> OclWrapper(True).oclIsUndefined()
        False
        >>> OclWrapper(None).oclIsUndefined()
        True
        """
        return self._wrapped is None


class OclWrapper_Extended(OclWrapper):
    """ Example of OclWrapper with additionnal functionnality """

    def sayHello(self):
        print("Hello from ", self._wrapped, "!")






class OclWrapper_String(OclWrapper):

    def concat(self, otherObject: object) -> OclWrapper_String:
        """Concatenates the other object (eventually already wrapped) to the wrapped string.

        Note:
            OCL functionnality -> 'concat'

        Args:
            otherObject (object): The other object to concatenate to the wrapped object.

        Returns:
            An OclWrapper_String wrapping the original wrapped object concatenated with the other object (eventually already wrapped).

        >>> print(OclWrapper_String('Hello World!').concat(' I am a string.'))
        Hello World! I am a string.
        >>> print(OclWrapper_String('Hello World!').concat(OclWrapper_String(' I am another string.')))
        Hello World! I am another string.
        """
        return OclWrapper_String(self._wrapped + otherObject)

    def size(self) -> int:
        """Returns the size, aka le length, of the wrapped object.

        Note:
            OCL functionnality -> 'size'

        Returns:
            The size, aka le length, of the wrapped object.

        >>> OclWrapper_String('Hello World!').size()
        12
        >>> OclWrapper_String('').size()
        0
        >>> OclWrapper_String(OclWrapper('Hello World!')).size()
        12
        """
        return len(self._wrapped)







"""
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
"""
"""
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
"""
"""
# Ocl functionnality -> oclIsKindOf
a = OclWrapper("a")
b = OclWrapper_Extended(1)
print(a.oclIsKindOf(OclWrapper))
print(a.oclIsKindOf(OclWrapper_Extended))
print(b.oclIsKindOf(OclWrapper))
print(b.oclIsKindOf(OclWrapper_Extended))
"""
"""
# Ocl functionnality -> oclIsTypeOf
a = OclWrapper("a")
b = OclWrapper_Extended(1)
print(a.oclIsTypeOf(OclWrapper))
print(a.oclIsTypeOf(OclWrapper_Extended))
print(b.oclIsTypeOf(OclWrapper))
print(b.oclIsTypeOf(OclWrapper_Extended))
"""
"""
# Ocl functionnality -> oclIsInvalid
a = OclWrapper("a")
b = OclWrapper_Extended(None)
print(a.oclIsInvalid())
print(b.oclIsInvalid())
"""
"""
# Ocl functionnality -> oclIsUndefined
a = OclWrapper("a")
b = OclWrapper_Extended(None)
print(a.oclIsUndefined())
print(b.oclIsUndefined())
"""
"""
# Ocl functionnality -> concat
astr = OclWrapper_String('Hello World!')
print(astr.concat(' I\'m a string.'))
print(astr.concat(OclWrapper_String(' I\'m a another string.')))
"""
"""
# Ocl functionnality -> size
print(OclWrapper_String('Hello World!').size())
print(OclWrapper_String(OclWrapper('Hello World!')).size())
"""


if __name__ == '__main__':
    doctest.testmod()
