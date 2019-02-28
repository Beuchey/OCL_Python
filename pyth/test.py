# Function definition is here
def changeme( list ):
    """This a docstring describing the function."""
    list.append([1,2,3,4]);
    return list

def add( x ):
    return x+3

def fibo( x, y, z ):
    while y < z :
        print(x)
        x, y = y, x+y

# Now you can call changeme function
print("Res:\n", changeme( [10,20,30] ))
print("Res:\n", add( 3 ))
print("Res:")
fibo(0,1,40)




words = ['cat', 'window', 'defenestrate']
for w in words[:]:  # Loop over a slice copy of the entire list, if not a copy then loops forever.
    if len(w) > 6:
        words.insert(0, w)

print(words)


for i in range(5):
    print(i)
print("-------")
for i in range(5,10):
    print(i)
print("-------")
for i in range(0,10,3):
    print(i)
print("-------")
for i in range(-10,-100,-30):
    print(i)


a = ['Mary', 'had', 'a', 'little', 'lamb']
for i in range(len(a)):
    print(i, a[i])
print(range(10))

f = fibo
f(2,4,50)

def concat(*args,sep="/"):
    return sep.join(args)
print(concat("earth", "mars", "venus"))
print(concat("earth", "mars", "venus", sep="."))

def incrementor_maker(step):
    return lambda x: x + step
f = incrementor_maker(42)
print(f(0))
print(f(1))

# Function avec annotations sur le type des parametres :
def afoo(cheese: str, meat: str = "ham") -> str:
    """This a docstring describing the function."""
    print("Annotations:", afoo.__annotations__)
    print("Arguments:", cheese, meat)
    return cheese + ' and ' + meat
print(afoo('camembert'), end=" <- put this on pancakes\n")
print(afoo('brie', 'bacon'), end=" <- put this on bread\n")

print(list(map(lambda x: x**2, range(10))))
print([x**3 for x in range(10)])
print([(x,y,x+y) for x in [1,2,3] for y in [3,1,4] if x != y])
from math import pi
print([str(round(pi, i)) for i in range(1, 6)])
