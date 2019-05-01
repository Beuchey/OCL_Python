someValue = open("test.txt",'w+')

condition = True

class Test():
  base = [0, lambda x,y : x+y, 2, 3, 4, 5]
  def __add__(self, other):
      return other+1
  def __radd__(self, other):
    return other+1

name0 = Test()
name1 = 0

qualifier1 = 1
qualifier2 = 2

aParameter = 3

multiple = 4
summable = 5

aValue = [0, 1, 2, 3, 4, 5, 6, 7, 8]

aqualifier = 7

aBoolean = False

anotherOne = 8

two = 2

enum = 9

path = 10
