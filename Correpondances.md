# Classifier

|OCL expression|OCL parameter(s)|OCL return type|Python3 target|Python3 expression|Python3 parameter(s)|Python3 return type|
| - | - | - | - | - | - | - |
|allInstances||Set{T}|classinfo|__instances = set()||set()|

# OclAny
|OCL expression|OCL parameter(s)|OCL return type|Python3 target|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - | - |
|oclAsType|t : Classifier|t|object|if(isinstance(self, aclass)): return self|classinfo|{self, None}|
|oclIsKindOf|Classifier|Boolean|object|return isinstance(self, aclass)|classinfo|{True, False}|
|oclIsInvalid||Boolean|object|return self._wrapped is None||{True, False}|
|oclIsTypeOf|t : Classifier|Boolean|object|return type(self) is aclass|classinfo|{True, False}|
|oclIsUndefined||Boolean|object|return self._wrapped is None||{True, False}|
|<>|OclAny|Boolean|object|!=|object|{True, False}|
|=|OclAny|Boolean|object|==|object|{True, False}|
|<|T|Boolean|object|<|object|{True, False}|
|>|T|Boolean|object|>|object|{True, False}|
|<=|T|Boolean|object|<=|object|{True, False}|
|>=|T|Boolean|object|>=|object|{True, False}|
# String
|OCL expression|OCL parameter(s)|OCL return type|Python3 target|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - | - |
|concat|String|String|||||
|size||Integer|||||
|substring|lower:Integer,upper:Integer|String|||||
|toInteger||Integer|||||
|toLower||String|||||
|toReal||Real|||||
|toUpper||String|||||
# Number
|OCL expression|OCL parameter(s)|OCL return type|Python3 target|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - | - |
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

|OCL expression|OCL parameter(s)|OCL return type|Python3 target|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - | - |
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
|OCL expression|OCL parameter(s)|OCL return type|Python3 target|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - | - |
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
|OCL expression|OCL parameter(s)|OCL return type|Python3 target|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - | - |
|=|Bag{T}|Boolean|||||
|<>|Bag{T}|Boolean|||||
|intersection|Bag{T}|Bag{T}|||||
|intersection|Set{T}|Set{T}|||||
|union|Bag{T}|Bag{T}|||||
|union|Set{T}|Set{T}|||||
# OrderedSet{T}
|OCL expression|OCL parameter(s)|OCL return type|Python3 target|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - | - |
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
|OCL expression|OCL parameter(s)|OCL return type|Python3 target|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - | - |
|=|Set{T}|Boolean|||||
|<>|Set{T}|Boolean|||||
|-|Set{T}|Set{T}|||||
|intersection|Bag{T}|Set{T}|||||
|intersection|Set{T}|Set{T}|||||
|symmetricDifference|Set{T}|Set{T}|||||
|union|Bag{T}|Bag{T}|||||
|union|Set{T}|Set{T}|||||
# Boolean
|OCL expression|OCL parameter(s)|OCL return type|Python3 target|Python3 expression|Python3 parameter(s)|Python3 return type
|-| - | - | - | - | - | - |
|And|Boolean|Boolean|||||
|Implies|Boolean|Boolean|||||
|Or|Boolean|Boolean|||||
|Not|Boolean|Boolean|||||
|Xor|Boolean|Boolean|||||
