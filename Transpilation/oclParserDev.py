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
            contentType = type(content)
            if(contentType==list or contentType==str):
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
    to.write(tabl)
    for e in args:
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
    log(level, "FOUND : ", expressionDescription, " : \n", tabulate(level+1), filter(expression), "\n")

def delegate(elements, identifier, level):
    log(level+1, "***", identifier, " : ")
    content = elements[identifier]
    if(type(content)==list):
        return defaultExpressionParser(content[0], level+1)
    else:
        return defaultExpressionParser(content, level+1)

def splitInfix(elements, operatorName, leftExpressionName, rightExpressionName, level):
    operator = elements[operatorName]
    if operator is not None and len(operator)==1:
        return delegate(elements, leftExpressionName, level) + " " + operator[0] + " " + delegate(elements, rightExpressionName, level)
    else:
        return delegate(elements, leftExpressionName, level)




# Parse tools

metamodel = metamodel_from_file("oclGrammar.tx")

def extractAtribute(e):
    elements = vars(e)
    for i in elements:
        if elements[i] is not None:
            return elements[i]

@singledispatch
def defaultExpressionParser(expression, level):
    #introduce(expression, "DefaultExpression", level)
    return "X"

@defaultExpressionParser.register(metamodel["IfExpression"])
def ifExpressionParser(expression, level):
    introduce(expression, "IfExpression", level)
    elements = vars(expression)
    return delegate(elements, "thenExpression", level) + " if " + delegate(elements, "conditionExpression", level) + " else " + delegate(elements, "elseExpression", level)

@defaultExpressionParser.register(metamodel["LogicalExpression"])
def logicalExpressionParser(expression, level):
    introduce(expression, "LogicalExpression", level)
    elements = vars(expression)
    return splitInfix(elements, "logicalOperator", "leftRelationalExpression", "rightRelationalExpression", level)

@defaultExpressionParser.register(metamodel["LetExpression"])
def letExpressionParser(expression, level):
    introduce(expression, "LetExpression", level)
    elements = vars(expression)
    return "with " + delegate(elements, "initExpression", level) + " as " + elements["identifier"] + " :\n" + tabulate(level+1) + delegate(elements, "subExpression", level)

@defaultExpressionParser.register(metamodel["RelationalExpression"])
def relationalExpressionParser(expression, level):
    introduce(expression, "RelationalExpression", level)
    elements = vars(expression)
    return splitInfix(elements, "relationalOperator", "leftAdditiveExpression", "rightAdditiveExpression", level)

@defaultExpressionParser.register(metamodel["AdditiveExpression"])
def additiveExpressionParser(expression, level):
    introduce(expression, "additiveExpression", level)
    elements = vars(expression)
    return splitInfix(elements, "additiveOperator", "leftMultiplicativeExpression", "rightMultiplicativeExpression", level)

@defaultExpressionParser.register(metamodel["MultiplicativeExpression"])
def multiplicativeExpressionParser(expression, level):
    introduce(expression, "multiplicativeExpression", level)
    elements = vars(expression)
    return splitInfix(elements, "multiplyOperator", "leftUnaryExpression", "rightUnaryExpression", level)

@defaultExpressionParser.register(metamodel["UnaryExpression"])
def unaryExpressionParser(expression, level):
    introduce(expression, "UnaryExpression", level)
    elements = vars(expression)
    if(elements["unaryOperator"] is None):
        return delegate(elements, "postfixExpression", level)
    else:
        return elements["unaryOperator"] + " " + delegate(elements, "postfixExpression", level)

@defaultExpressionParser.register(metamodel["PostfixExpression"])
def unaryExpressionParser(expression, level):
    introduce(expression, "PostfixExpression", level)
    elements = vars(expression)
    return delegate(elements, "primaryExpression", level)

@defaultExpressionParser.register(metamodel["PropertyCall"])
def propertyCallParser(expression, level):
    introduce(expression, "PropertyCall", level)
    elements = vars(expression)
    return delegate(elements, "pathName", level)

@defaultExpressionParser.register(metamodel["PathName"])
def pathNameParser(expression, level):
    introduce(expression, "PathName", level)
    return vars(expression)["names"][0]






# WHERE THE MAGIC HAPPENS

model = metamodel.model_from_file("expression.ocl")

for expression in model.expressions:
    res(0, defaultExpressionParser(expression, 0), "\n")






logger.close()
result.close()
