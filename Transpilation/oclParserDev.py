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
    tabl = tabulate(level)
    for e in args:
        to.write(tabl)
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
    writeTo(result, 0, *args)

def introduce(expression, expressionDescription, level):
    log(level, expressionDescription, " : \n", tabulate(level+1), filter(expression), "\n")

def delegate(elements, identifier, level):
    log(level+1, "***", identifier, " : ")
    return defaultExpressionParser(elements[identifier], level+1)





# Parse tools

metamodel = metamodel_from_file("oclGrammar.tx")

def extractAtribute(e):
    elements = vars(e)
    for i in elements:
        if elements[i] is not None:
            return elements[i]

@singledispatch
def defaultExpressionParser(expression, level):
    introduce(expression, "DefaultExpression", level)
    return ""

@defaultExpressionParser.register(metamodel["IfExpression"])
def ifExpressionParser(expression, level):
    introduce(expression, "IfExpression", level)
    elements = vars(expression)
    return delegate(elements, "thenExpression", level) + " if " + delegate(elements, "conditionExpression", level) + " else " + delegate(elements, "elseExpression", level)

@defaultExpressionParser.register(metamodel["LogicalExpression"])
def logicalExpressionParser(expression, level):
    introduce(expression, "LogicalExpression", level)
    return "LogicalExpression"

@defaultExpressionParser.register(metamodel["LetExpression"])
def letExpressionParser(expression, level):
    introduce(expression, "LetExpression", level)
    elements = vars(expression)
    return "with " + delegate(elements, "initExpression", level) + " as " + elements["identifier"] + " in "








# WHERE THE MAGIC HAPPENS

model = metamodel.model_from_file("expression.ocl")

for expression in model.expressions:
    res(0, defaultExpressionParser(expression, 0), "\n")






logger.close()
result.close()
