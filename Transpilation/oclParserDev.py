from sys import __stdout__

from functools import singledispatch

from textx import metamodel_from_file
from textx.model import get_metamodel










# Output tools

def filter(expression):
    elements = vars(expression)
    result = {}
    for e in elements:
        if e is not None and e[0]!='_' and e!='parent':
            content = elements[e]
            if(type(content)==list):
                result[e] = content
            else:
                result[e] = content.__class__.__name__
    return result

def tabulate(level):
    res = ""
    for i in range(level):
        res += "\t"
    return res

def writeTo(to, level, *args):
    for e in args:
        to.write(tabulate(level))
        to.write(str(e))
    to.write("\n")

logger = open("log.txt","w+")

VERBOSE = True

def log(level, *args):
    writeTo(logger, level, *args)
    if(VERBOSE):
        writeTo(__stdout__, level, *args)


result = open("result.txt","w+")

def res(level, *args):
    writeTo(logger, *args)








# Parse tools

metamodel = metamodel_from_file("oclGrammar.tx")

def extractAtribute(e):
    elements = vars(e)
    for i in elements:
        if elements[i] is not None:
            return elements[i]

@singledispatch
def defaultExpressionParser(expression, level):
    log(level, "Default : \n", tabulate(level+1), filter(expression))

@defaultExpressionParser.register(metamodel["IfExpression"])
def ifExpressionParser(expression, level):
    log(level, "IfExpression : \n", tabulate(level+1), filter(expression), "\n")
    elements = vars(expression)
    log(level+1, "*** conditionExpression : ")
    defaultExpressionParser(elements["conditionExpression"], level+1)
    log(level+1, "*** thenExpression : ")
    defaultExpressionParser(elements["thenExpression"], level+1)
    log(level+1, "*** elseExpression : ")
    defaultExpressionParser(elements["elseExpression"], level+1)

@defaultExpressionParser.register(metamodel["LogicalExpression"])
def logicalExpressionParser(expression, level):
    log(level, "LogicalExpression : \n", tabulate(level+1), filter(expression), "\n")








# WHERE THE MAGIC HAPPENS

model = metamodel.model_from_file("expression.ocl")

for expression in model.expressions:
    defaultExpressionParser(expression, 0)









logger.close()
result.close()
