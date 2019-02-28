# oclIsInvalid

Use a wrapper with "is None".

```Python
class Wrapper(object):

    def __init__(self, awrapped : object):
        self.wrapped = awrapped

    def oclIsInvalid(self):
        return self.wrapped is None



a = Wrapper("2")
b = Wrapper(None)

print(a.oclIsInvalid())
print(b.oclIsInvalid())
```
