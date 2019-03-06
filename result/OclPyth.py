# -*- coding: utf-8 -*-
from __future__ import annotations # To be able to return the current class in class method. This import should become unnecessary in Python 4.0 to be able to di this.
import doctest
import weakref
from math import trunc, floor, ceil
from sys import stdout

class OclWrapper(object):
    """ A wrapper for any other objects to which we need to add functionnalities in order to match Ocl's """

    # Class attributes

    __slots__ = ['__weakref__', '_wrapped']
    """
        Use __slots__ method to store attributes for class instances :
        Prevents from the default Python's behaviour to use a dictionnary to store them and
        so allow to dynamically add, modify or delate attributes to each instances, but loosing
        performance.
        Use slots instead disallow to add, modify or delate attributes to each instances, but gains
        in performance.

        We need to add '__weakref__' in order to allow weak references on class instances.

        We need to also declare each possible instance attribute, like the wrapped object '_wrapped'.
    """

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

    def __bytes__(self) -> bytes:
        """__bytes__ method.

        Note:
            Delegates the __bytes__ method to the wrapped object.

        Returns:
            The result of the operation on the wrapped object.

        >>> print(bytes(OclWrapper(True)))
        b'\\x00'
        >>> print(bytes(OclWrapper(False)))
        b''
        >>> print(bytes(OclWrapper(1)))
        b'\\x00'
        >>> print(bytes(OclWrapper((1, 16, 10))))
        b'\\x01\\x10\\n'
        >>> print(bytes(OclWrapper([1, 16, 10])))
        b'\\x01\\x10\\n'
        """
        return bytes(self._wrapped)

    def __format__(self, *format_spec: str) -> str:
        """__format__ method.

        Note:
            Delegates the __format__ method to the wrapped object.

        Returns:
            The result of the operation on the wrapped object.

        >>> OclWrapper('Hello {0}, I am {1}').format('world', 'John')
        'Hello world, I am John'
        >>> OclWrapper('User ID: {uid}   Last seen: {last_login}').format(uid="root", last_login = "5 Mar 2008 07:20")
        'User ID: root   Last seen: 5 Mar 2008 07:20'
        >>> OclWrapper('Empty dict: {{}}').format()
        'Empty dict: {}'
        >>> OclWrapper('Item 1: {0[1]}   Item 2: {0[2]}').format((4, 12, 5))
        'Item 1: 12   Item 2: 5'
        """
        return self._wrapped.__format__(*format_spec)

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
        return OclWrapper(otherObject ^ self._wrapped)

    def __iadd__(self, otherObject) -> OclWrapper:
        """__iadd__ method.

        Note:
            Delegates the __iadd__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "iadd" this one.

        Returns:
            Updates the wrapped object with the operation and returns self.

        >>> a = OclWrapper(1)
        >>> a += 2
        >>> print(a)
        3
        >>> a = OclWrapper(1)
        >>> a += OclWrapper(2)
        >>> print(a)
        3
        >>> a = OclWrapper('Hello')
        >>> a += ' world!'
        >>> print(a)
        Hello world!
        >>> a = OclWrapper('Hello')
        >>> a += OclWrapper(' world!')
        >>> print(a)
        Hello world!
        >>> a = OclWrapper((1, 2))
        >>> a += (3, 4)
        >>> print(a)
        (1, 2, 3, 4)
        >>> a = OclWrapper((1, 2))
        >>> a += OclWrapper((3, 4))
        >>> print(a)
        (1, 2, 3, 4)
        >>> a = OclWrapper([1, 2])
        >>> a += [3, 4]
        >>> print(a)
        [1, 2, 3, 4]
        >>> a = OclWrapper([1, 2])
        >>> a += OclWrapper([3, 4])
        >>> print(a)
        [1, 2, 3, 4]
        """
        object.__setattr__(self, '_wrapped', self._wrapped + otherObject)
        return self

    def __isub__(self, otherObject) -> OclWrapper:
        """__isub__ method.

        Note:
            Delegates the __isub__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "isub" this one.

        Returns:
            Updates the wrapped object with the operation and returns self.

        >>> a = OclWrapper(1)
        >>> a -= 2
        >>> print(a)
        -1
        >>> a = OclWrapper(1)
        >>> a -= OclWrapper(2)
        >>> print(a)
        -1
        """
        object.__setattr__(self, '_wrapped', self._wrapped - otherObject)
        return self

    def __imul__(self, otherObject) -> OclWrapper:
        """__imul__ method.

        Note:
            Delegates the __imul__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "imul" this one.

        Returns:
            Updates the wrapped object with the operation and returns self.

        >>> a = OclWrapper(1)
        >>> a *= 2
        >>> print(a)
        2
        >>> a = OclWrapper(1)
        >>> a *= OclWrapper(2)
        >>> print(a)
        2
        """
        object.__setattr__(self, '_wrapped', self._wrapped * otherObject)
        return self

    def __imatmul__(self, otherObject) -> OclWrapper:
        """__imatmul__ method.

        Note:
            Delegates the __imatmul__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "imatmul" this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.
        """
        object.__setattr__(self, '_wrapped', self._wrapped @ otherObject)
        return self

    def __itruediv__(self, otherObject) -> OclWrapper:
        """__itruediv__ method.

        Note:
            Delegates the __itruediv__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "itruediv" this one.

        Returns:
            Updates the wrapped object with the operation and returns self.

        >>> a = OclWrapper(1)
        >>> a /= 2
        >>> print(a)
        0.5
        >>> a = OclWrapper(1)
        >>> a /= OclWrapper(2)
        >>> print(a)
        0.5
        """
        object.__setattr__(self, '_wrapped', self._wrapped / otherObject)
        return self

    def __ifloordiv__(self, otherObject) -> OclWrapper:
        """__ifloordiv__ method.

        Note:
            Delegates the __ifloordiv__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "ifloordiv" this one.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> a = OclWrapper(1)
        >>> a //= 2
        >>> print(a)
        0
        >>> a = OclWrapper(1)
        >>> a //= OclWrapper(2)
        >>> print(a)
        0
        """
        object.__setattr__(self, '_wrapped', self._wrapped // otherObject)
        return self

    def __imod__(self, otherObject) -> OclWrapper:
        """__imod__ method.

        Note:
            Delegates the __imod__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "imod" this one.

        Returns:
            Updates the wrapped object with the operation and returns self.

        >>> a = OclWrapper(7)
        >>> a %= 2
        >>> print(a)
        1
        >>> a = OclWrapper(7)
        >>> a %= OclWrapper(2)
        >>> print(a)
        1
        """
        object.__setattr__(self, '_wrapped', self._wrapped % otherObject)
        return self

    def __ipow__(self, otherObject) -> OclWrapper:
        """__ipow__ method.

        Note:
            Delegates the __ipow__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "ipow" this one.

        Returns:
            Updates the wrapped object with the operation and returns self.

        >>> a = OclWrapper(2)
        >>> a **= 3
        >>> print(a)
        8
        >>> a = OclWrapper(2)
        >>> a **= OclWrapper(3)
        >>> print(a)
        8
        """
        object.__setattr__(self, '_wrapped', self._wrapped ** otherObject)
        return self

    def __ilshift__(self, otherObject) -> OclWrapper:
        """__ilshift__ method.

        Note:
            Delegates the __ilshift__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "ilshift" this one.

        Returns:
            Updates the wrapped object with the operation and returns self.

        >>> a = OclWrapper(1)
        >>> a <<= 2
        >>> print(a)
        4
        >>> a = OclWrapper(1)
        >>> a <<= OclWrapper(2)
        >>> print(a)
        4
        """
        object.__setattr__(self, '_wrapped', self._wrapped << otherObject)
        return self

    def __irshift__(self, otherObject) -> OclWrapper:
        """__irshift__ method.

        Note:
            Delegates the __irshift__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "irshift" this one.

        Returns:
            Updates the wrapped object with the operation and returns self.

        >>> a = OclWrapper(2)
        >>> a >>= 1
        >>> print(a)
        1
        >>> a = OclWrapper(2)
        >>> a >>= OclWrapper(1)
        >>> print(a)
        1
        """
        object.__setattr__(self, '_wrapped', self._wrapped >> otherObject)
        return self

    def __iand__(self, otherObject) -> OclWrapper:
        """__iand__ method.

        Note:
            Delegates the __iand__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "iand" this one.

        Returns:
            Updates the wrapped object with the operation and returns self.

        >>> a = OclWrapper(3)
        >>> a &= 1
        >>> print(a)
        1
        >>> a = OclWrapper(3)
        >>> a &= OclWrapper(1)
        >>> print(a)
        1
        """
        object.__setattr__(self, '_wrapped', self._wrapped & otherObject)
        return self

    def __ior__(self, otherObject) -> OclWrapper:
        """__ior__ method.

        Note:
            Delegates the __ior__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "ior" this one.

        Returns:
            Updates the wrapped object with the operation and returns self.

        >>> a = OclWrapper(3)
        >>> a |= 1
        >>> print(a)
        3
        >>> a = OclWrapper(3)
        >>> a |= OclWrapper(1)
        >>> print(a)
        3
        """
        object.__setattr__(self, '_wrapped', self._wrapped | otherObject)
        return self

    def __ixor__(self, otherObject) -> OclWrapper:
        """__ixor__ method.

        Note:
            Delegates the __ixor__ method to the wrapped object and creates an OclWrapper.

        Args:
            otherObject (object): The other object to "ixor" this one.

        Returns:
            Updates the wrapped object with the operation and returns self.

        >>> a = OclWrapper(3)
        >>> a ^= 1
        >>> print(a)
        2
        >>> a = OclWrapper(3)
        >>> a ^= OclWrapper(1)
        >>> print(a)
        2
        """
        object.__setattr__(self, '_wrapped', self._wrapped ^ otherObject)
        return self

    def __neg__(self) -> OclWrapper:
        """__neg__ method.

        Note:
            Delegates the __neg__ method to the wrapped object and creates an OclWrapper.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(-OclWrapper(3))
        -3
        >>> print(-OclWrapper(-3))
        3
        """
        return OclWrapper(-self._wrapped)

    def __pos__(self) -> OclWrapper:
        """__pos__ method.

        Note:
            Delegates the __pos__ method to the wrapped object and creates an OclWrapper.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(+OclWrapper(3))
        3
        >>> print(+OclWrapper(-3))
        -3
        """
        return OclWrapper(+self._wrapped)

    def __abs__(self) -> OclWrapper:
        """__abs__ method.

        Note:
            Delegates the __abs__ method to the wrapped object and creates an OclWrapper.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(abs(OclWrapper(3)))
        3
        >>> print(abs(OclWrapper(-3)))
        3
        """
        return OclWrapper(abs(self._wrapped))

    def __invert__(self) -> OclWrapper:
        """__invert__ method.

        Note:
            Delegates the __invert__ method to the wrapped object and creates an OclWrapper.

        Returns:
            An OclWrapper wrapping the result of the operation on the wrapped object and the other object.

        >>> print(~OclWrapper(3))
        -4
        >>> print(~OclWrapper(-3))
        2
        """
        return OclWrapper(~self._wrapped)

    def __int__(self) -> int:
        """__int__ method.

        Note:
            Delegates the __int__ method to the wrapped object.

        Returns:
            The result of the operation on the wrapped object and the other object.

        >>> print(int(OclWrapper(3)))
        3
        >>> print(int(OclWrapper(3.5)))
        3
        """
        return int(self._wrapped)

    def __float__(self) -> float:
        """__float__ method.

        Note:
            Delegates the __int__ method to the wrapped object.

        Returns:
            The result of the operation on the wrapped object and the other object.

        >>> print(float(OclWrapper(3)))
        3.0
        >>> print(float(OclWrapper(3.5)))
        3.5
        """
        return float(self._wrapped)

    def __complex__(self) -> complex:
        """__complex__ method.

        Note:
            Delegates the __complex__ method to the wrapped object.

        Returns:
            The result of the operation on the wrapped object and the other object.

        >>> print(complex(OclWrapper(3)))
        (3+0j)
        >>> print(complex(OclWrapper(3.5)))
        (3.5+0j)
        """
        return complex(self._wrapped)

    def __index__(self) -> int:
        """__index__ method.

        Note:
            Delegates the __index__ method to the wrapped object.

            In order to have a coherent integer type class, when __index__() is defined __int__() should also be defined,
            and both should return the same value.

        Returns:
            The result of the operation on the wrapped object and the other object.

        >>> print(OclWrapper(3).__index__())
        3
        """
        return self._wrapped.__index__()

    def __round__(self, *ndigits) -> real:
        """__round__ method.

        Note:
            Delegates the __round__ method to the wrapped object.

        Returns:
            The result of the operation on the wrapped object and the other object.

        >>> print(round(OclWrapper(3)))
        3
        >>> print(round(OclWrapper(3.111111)))
        3
        >>> print(round(OclWrapper(3.444444)))
        3
        >>> print(round(OclWrapper(3.555555)))
        4
        >>> print(round(OclWrapper(3.999999)))
        4
        >>> print(round(OclWrapper(3), 3))
        3
        >>> print(round(OclWrapper(3.111111), 3))
        3.111
        >>> print(round(OclWrapper(3.444444), 3))
        3.444
        >>> print(round(OclWrapper(3.555555), 3))
        3.556
        >>> print(round(OclWrapper(3.999999), 3))
        4.0
        """
        return self._wrapped.__round__(*ndigits)

    def __trunc__(self) -> int:
        """__trunc__ method.

        Note:
            Delegates the __trunc__ method to the wrapped object.

        Returns:
            The result of the operation on the wrapped object and the other object.

        >>> print(trunc(OclWrapper(3)))
        3
        >>> print(trunc(OclWrapper(3.1)))
        3
        >>> print(trunc(OclWrapper(3.4)))
        3
        >>> print(trunc(OclWrapper(3.5)))
        3
        >>> print(trunc(OclWrapper(3.9)))
        3
        """
        return self._wrapped.__trunc__()

    def __floor__(self) -> int:
        """__floor__ method.

        Note:
            Delegates the __floor__ method to the wrapped object.

        Returns:
            The result of the operation on the wrapped object and the other object.

        >>> print(floor(OclWrapper(3)))
        3
        >>> print(floor(OclWrapper(3.1)))
        3
        >>> print(floor(OclWrapper(3.4)))
        3
        >>> print(floor(OclWrapper(3.5)))
        3
        >>> print(floor(OclWrapper(3.9)))
        3
        """
        return floor(self._wrapped)

    def __ceil__(self) -> int:
        """__ceil__ method.

        Note:
            Delegates the __ceil__ method to the wrapped object.

        Returns:
            The result of the operation on the wrapped object and the other object.

        >>> print(ceil(OclWrapper(3)))
        3
        >>> print(ceil(OclWrapper(3.1)))
        4
        >>> print(ceil(OclWrapper(3.4)))
        4
        >>> print(ceil(OclWrapper(3.5)))
        4
        >>> print(ceil(OclWrapper(3.9)))
        4
        """
        return ceil(self._wrapped)

    # Emulating context manager

    def __enter__(self) -> object:
        """__enter__ method.

        Note:
            If the wrapped object has an __enter__ attribute, delegates the operation to it,
            or returns directly the wrapped object if it has not.

        >>> with OclWrapper(True) as o: print(o)
        True
        >>> with OclWrapper(OclWrapper(False)) as o: print(o)
        False
        """
        try:
            return self._wrapped.__enter__()
        except AttributeError:
            return self._wrapped

    def __exit__(self, exception_type, exception_value, exception_traceback) -> bool:
        """__exit__ method.

        Note:
            Delegates the __exit__ method to the wrapped object.

            If an exception is supplied, and the method wishes to suppress the exception
            (i.e., prevent it from being propagated), it should return a true value.
            Otherwise, the exception will be processed normally upon exit from this method.
        """
        return False

    # Emulating descriptors

    def __get__(self, instance: object, owner: str) -> object:
        """Called when we call __getattr__ on an instance of a class, or directly on a class,
            owning an attribute instance of this class, that we are trying to access to.

            The default behaviour is to simply return self (allow simple access),
            but this may be customized.

        Args:
            instance (objet): the instance through wich the call has been made
            (None if the call has been made directly through the class itself).

            owner (str): Class through which the call has been made, directly or from an instance.

        Returns:
            The value asked, eventully computed.
        """
        try:
            return self._wrapped.__get__(instance, owner)
        except AttributeError:
            return self

    def __set__(self, instance: object, value: object):
        """Called when we call __setattr__ on an instance of a class, or directly on a class,
            owning an attribute instance of this class, that we are trying to access to.

            The default behaviour is to simply modify self (allow simple modification),
            but this may be customized.
            For example, a read-only descriptor could raise an AttributeError in its
            __set__ method do disallow any setting of an instance of this class.

            Example: If the class MyClass defines __set__, the in any call, on an instance I of
            MyClass ou directly on MyClass, like "I = qqch", it will be this __set__ method
            that will be called, instead of simply modify I's value.

            This allows, for example, to perform in-place modifications instead of replace
            the all value of an instance, or to create restrictions about which values
            the instances can have.

        Args:
            instance (objet): the instance through wich the call has been made
            (None if the call has been made directly through the class itself).

            value (str): The new value concerning the modification.
        """
        try:
            return self._wrapped.__set__(instance, value)
        except AttributeError:
            return object.__setattr__(self, '_wrapped', value)

    def __delete__(self, instance: object):
        """Called when we call __delattr__ on an instance of a class, or directly on a class,
            owning an attribute instance of this class, that we are trying to access to.

            The default behaviour is to do nothing (allow simple deletion),
            but this may be customized.

        Args:
            instance (objet): the instance through wich the call has been made
            (None if the call has been made directly through the class itself).

            value (str): The new value concerning the modification.
        """
        try:
            self._wrapped.__delete__(instance)
        except AttributeError:
            pass

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

    def substring(self, start: int, end: int) -> str:
        """Slices the _wrapped object from start to end.

        Note:
            In OCL, indexes like in Strings begin at 1, not 0, and OCL's substring includes the end index in the result.

            OCL functionnality -> 'substring'

        Args:
            start (integer): The first element index to include (starting at 1)
            end (integer): The last element index to include (starting at 1)

        Returns:
            The result of the slicing from start to end on the wrapped object.

        >>> print(OclWrapper_String('test').substring(1,1))
        t
        >>> print(OclWrapper_String(OclWrapper_String('test')).substring(2,4))
        est
        >>> s = OclWrapper_String('test')
        >>> print(s.substring(1, s.size()))
        test
        """
        return self._wrapped[start-1:end]

    def toInteger(self) -> int:
        """Parses a String into an Integer, if possible.

        Note:
            OCL functionnality -> 'toInteger'

        Returns:
            The Integer value of the wrapped object.

        >>> print(OclWrapper_String('3').toInteger())
        3
        >>> print(OclWrapper_String(OclWrapper_String('3')).toInteger())
        3
        """
        return int(self._wrapped)





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
"""
# Ocl functionnality -> substring
print(OclWrapper_String('test').substring(1,1))
print(OclWrapper_String(OclWrapper_String('test')).substring(2,4))
s = OclWrapper_String('test')
print(s.substring(1, s.size()))
"""
"""
# Ocl functionnality -> toInteger
print(OclWrapper_String('3').toInteger())
print(OclWrapper_String(OclWrapper_String('3')).toInteger())
"""




if __name__ == '__main__':
    doctest.testmod()
