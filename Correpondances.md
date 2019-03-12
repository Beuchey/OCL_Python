# Classifier -> OclWrapper_Any (object)

|OCL expression|OCL parameter(s)|OCL return type|Python3 expression|Python3 parameter(s)|Python3 return type|
| - | - | - | - | - | - |
|allInstances||Set{T}|`__instances = set()`||set()|

# OclAny -> OclWrapper_Any (object)

|OCL expression|OCL parameter(s)|OCL return type|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - |
|oclAsType|t : Classifier|t|`if(isinstance(self, aclass)): return self`|classinfo|{self, None}|
|oclIsKindOf|Classifier|Boolean|`isinstance(self, aclass)`|classinfo|{True, False}|
|oclIsInvalid||Boolean|`self._wrapped is None`||{True, False}|
|oclIsTypeOf|t : Classifier|Boolean|`type(self) is aclass`|classinfo|{True, False}|
|oclIsUndefined||Boolean|`self._wrapped is None`||{True, False}|
|<>|OclAny|Boolean|`__ne__`|object|{True, False}|
|=|OclAny|Boolean|`__eq__` (and so `__hash__`)|object|{True, False}|
|<|T|Boolean|`__lt__`|object|{True, False}|
|>|T|Boolean|`__gt__`|object|{True, False}|
|<=|T|Boolean|`__le__`|object|{True, False}|
|>=|T|Boolean|`__ge__`|object|{True, False}|

# String -> OclWrapper_String (str)

|OCL expression|OCL parameter(s)|OCL return type|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - |
|concat|String|String|`self._wrapped + otherObject`<br /><br />`self._wrapped + otherObject._wrapped`|object<br /><br />OCLWrapper|str|
|size||Integer|`len(self._wrapped)`||int|
|substring|lower:Integer,upper:Integer|String|`self._wrapped[start-1:end]`|start:int, end:int|str|
|toInteger||Integer|`int(self._wrapped)`||int|
|toLower||String|self._wrapped.lower()||str|
|toReal||Real||||
|toUpper||String||||

# Number

|OCL expression|OCL parameter(s)|OCL return type|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - |
|Number::abs||Number|||||
|Number::floor||Integer|||||
|Number::max|Number|Number|||||
|Number::min|Number|Number|||||
|Number::round||Integer|||||
|Number::div|Integer|Integer|||||

# Collections{T}

Please note that OCL collections can contain the *null* value (null) but not the *invalid* value (|invalid|). Trying to add |invalid| within a new or existing collection will yield |invalid| as a result. OCL proposes four distinct kinds of collections offering all possibilities of ordering/unicity.

|Collection type|Ordered|Unique
|-| - | - |
|Sequence|true|false
|OrderedSet|true|true
|Bag|false|false
|Set|false|true

|OCL expression|OCL parameter(s)|OCL return type|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - |
|any|OclExpression|T|||||
|asBag||Bag{T}|||||
|asOrderedSet||OrderedSet{T}|||||
|asSequence||Sequence{T}|||||
|asSet||Set{T}|||||
|collect|OclExpression|Collection{T2}|||||
|collectNested|OclExpression|Collection{T2}|||||
|count|T|Integer|||||
|excludes|T|Boolean|||||
|excludesAll|Collection{T}|Boolean|||||
|excluding|T|Collection{T}|||||
|exists|OclExpression|Boolean|||||
|flatten||Collection{T}|||||
|forAll|OclExpression|Boolean|||||
|includes|T|Boolean|||||
|includesAll|Collection{T}|Boolean|||||
|including|T|Collection{T}|||||
|isEmpty||Boolean|||||
|isUnique|OclExpression|Boolean|||||
|notEmpty||Boolean|||||
|one|OclExpression|Boolean|||||
|product|Collection{T2}|Set(Tuple(T,T2))|||||
|reject|OclExpression|Collection{T}|||||
|select|OclExpression|Collection{T}|||||
|size||Integer|||||
|sortedBy|OclExpression|Collection{T}|||||
|sum||Real|||||

# Sequence{T}

|OCL expression|OCL parameter(s)|OCL return type|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - |
|=|Sequence{T}|Boolean|||||
|<>|Sequence{T}|Boolean|||||
|append|T|Sequence{T}|||||
|at|Integer|T|||||
|first||T|||||
|indexOf|T|Integer|||||
|insertAt|Integer,T|Sequence{T}|||||
|last||T|||||
|prepend|T|Sequence{T}|||||
|subSequence|start:Integer,end:Integer|Sequence{T}|||||

# Bag{T}

|OCL expression|OCL parameter(s)|OCL return type|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - |
|=|Bag{T}|Boolean|||||
|<>|Bag{T}|Boolean|||||
|intersection|Bag{T}|Bag{T}|||||
|intersection|Set{T}|Set{T}|||||
|union|Bag{T}|Bag{T}|||||
|union|Set{T}|Set{T}|||||

# OrderedSet{T}

|OCL expression|OCL parameter(s)|OCL return type|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - |
|=|Set{T}|Boolean|||||
|=|OrderedSet{T}|Boolean|||||
|<>|Set{T}|Boolean|||||
|<>|OrderedSet{T}|Boolean|||||
|-|Set{T}|Set{T}|||||
|append|T|OrderedSet{T}|||||
|at|Integer|T|||||
|first||T|||||
|indexOf|T|Integer|||||
|insertAt|Integer,T|OrderedSet{T}|||||
|intersection|Bag{T}|Set{T}|||||
|intersection|Set{T}|Set{T}|||||
|last||T|||||
|prepend|T|OrderedSet{T}|||||
|subOrderedSet|start:Integer,end:Integer|OrderedSet{T}|||||
|symmetricDifference|Set{T}|Set{T}|||||
|union|Bag{T}|Bag{T}|||||
|union|Set{T}|Set{T}|||||

# Set{T}

|OCL expression|OCL parameter(s)|OCL return type|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - |
|=|Set{T}|Boolean|||||
|<>|Set{T}|Boolean|||||
|-|Set{T}|Set{T}|||||
|intersection|Bag{T}|Set{T}|||||
|intersection|Set{T}|Set{T}|||||
|symmetricDifference|Set{T}|Set{T}|||||
|union|Bag{T}|Bag{T}|||||
|union|Set{T}|Set{T}|||||

# Boolean

|OCL expression|OCL parameter(s)|OCL return type|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - |
|And|Boolean|Boolean|||||
|Implies|Boolean|Boolean|||||
|Or|Boolean|Boolean|||||
|Not|Boolean|Boolean|||||
|Xor|Boolean|Boolean|||||
