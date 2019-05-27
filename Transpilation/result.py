import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../Wrapper/', 'oclpyth'))
from oclWrapper import oclWrapper_Factory


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


#----------------------


with someValue as something :
		print(something) if condition else print(somethingElse)

not name0.base[ qualifier1 ](name0, name1 | aParameter) * multiple + summable

aValue[ aqualifier ] and (aBoolean or anotherOne)

oclWrapper_Factory([range(int(1), int(two)), range(int(len("three")), int(enum))])

path

oclWrapper_Factory([range(int(1.0))])

