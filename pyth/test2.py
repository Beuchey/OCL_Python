class MockObject(object):
    ''' A class representing any object, list, ... '''
    def __init__(self):
        self.unknownFieldForWrapperButKnownForWrapped = 'field accessed from wrapped'


class Proxy(object):
    ''' A wrapper for other objects '''

    def __init__(self, awrapped):
        self.wrapped = awrapped
        self.knownField = 'field accessed directly in wrapper'

    def __getattr__(self, attName):
        '''
        result = object.__getattribute__(self.wrapped, name)
        if isinstance(result, str):
            return StringProxy(result)
        if isinstance(result, list):
            return ProxyList(result)
        return Proxy(result)
        '''
        print(type(self), " : __getattr__ : ", attName)
        return object.__getattribute__(self.wrapped, attName)

    def __getattribute__(self, attName):
        '''
        if name == 'wrapped':
            return object.__getattribute__(self, 'wrapped')
        '''
        print(type(self), " : __getattribute__ : ", attName)
        return object.__getattribute__(self, attName)

    def oclIsKindOf(self, t):
        return isinstance(self.wrapped, t)


class StringProxy(Proxy):
    @property
    def length(self):
        return len(self.wrapped)

    def __eq__(self, value):
        return self.wrapped == value


class ListProxy(Proxy):
    def collect(self, func):
        return list(map(func,self.wrapped))

    def __getitem__(self, item):
        print(type(self), " : __getitem__ : ", item)
        return self.wrapped[item]






print()

t = MockObject()
p = Proxy(t)
print(p.knownField, end="\n\n")
print(p.unknownFieldForWrapperButKnownForWrapped, end="\n\n")

myString = StringProxy("Hello world!")
print(myString.knownField, end="\n\n")
print(myString.length, end="\n\n")
print(myString == "Hello world!", end="\n\n")
print(myString == "Goodbye world...", end="\n\n")

myList = ListProxy([1,2,3,4,5,6])
print(myList[3], end="\n\n")
print(list(myList.collect(lambda e: e*3)), end="\n\n")
