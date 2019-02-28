Assigner l'attribut __class__ de la cible :

```Python
from math import pi

class Circle(object):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return pi * self.radius**2

class CirclePlus(Circle):
    def diameter(self):
        return self.radius*2

    def circumference(self):
        return self.radius*2*pi

c = Circle(10)
print c.radius
print c.area()
print repr(c)

c.__class__ = CirclePlus
print c.diameter()
print c.circumference()
print repr(c)
```
