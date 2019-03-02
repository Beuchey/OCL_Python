class Wrapper(object):

    def __init__(self, awrapped : object):
        self.wrapped = awrapped

    def oclIsUndefined(self):
        return self.wrapped is None



a = Wrapper("2")
b = Wrapper(None)

print(a.oclIsUndefined())
print(b.oclIsUndefined())
