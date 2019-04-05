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
            if(contentType==list or contentType==str or contentType==int):
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











# Parse tools

metamodel = metamodel_from_file("oclGrammar.tx")






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

def extract(expression):
    elements = vars(expression)
    for e in elements:
        current = elements[e]
        if current is not None:
            return current








@singledispatch
def defaultExpressionParser(expression, level):
    log(level, "!!!DEFAULT!!!\n", tabulate(level+1), expression, "\n")
    return "!!!DEFAULT!!!"

@defaultExpressionParser.register(metamodel["Expression"])
def expressionParser(expression, level):
    introduce(expression, "Expression", level)
    return defaultExpressionParser(extract(expression), level+1)

@defaultExpressionParser.register(metamodel["IfExpression"])
def ifExpressionParser(expression, level):
    introduce(expression, "IfExpression", level)
    elements = vars(expression)
    return delegate(elements, "thenExpression", level) + " if " + delegate(elements, "conditionExpression", level) + " else " + delegate(elements, "elseExpression", level)

@defaultExpressionParser.register(metamodel["LogicalExpression"])
def logicalExpressionParser(expression, level):
    introduce(expression, "LogicalExpression", level)
    return splitInfix(vars(expression), "logicalOperator", "leftRelationalExpression", "rightRelationalExpression", level)

@defaultExpressionParser.register(metamodel["LetExpression"])
def letExpressionParser(expression, level):
    introduce(expression, "LetExpression", level)
    elements = vars(expression)
    return "with " + delegate(elements, "initExpression", level) + " as " + elements["identifier"] + " :\n" + tabulate(level+1) + delegate(elements, "subExpression", level)

@defaultExpressionParser.register(metamodel["RelationalExpression"])
def relationalExpressionParser(expression, level):
    introduce(expression, "RelationalExpression", level)
    return splitInfix(vars(expression), "relationalOperator", "leftAdditiveExpression", "rightAdditiveExpression", level)

@defaultExpressionParser.register(metamodel["AdditiveExpression"])
def additiveExpressionParser(expression, level):
    introduce(expression, "additiveExpression", level)
    return splitInfix(vars(expression), "additiveOperator", "leftMultiplicativeExpression", "rightMultiplicativeExpression", level)

@defaultExpressionParser.register(metamodel["MultiplicativeExpression"])
def multiplicativeExpressionParser(expression, level):
    introduce(expression, "multiplicativeExpression", level)
    return splitInfix(vars(expression), "multiplyOperator", "leftUnaryExpression", "rightUnaryExpression", level)

@defaultExpressionParser.register(metamodel["UnaryExpression"])
def unaryExpressionParser(expression, level):
    introduce(expression, "UnaryExpression", level)
    elements = vars(expression)
    if(elements["unaryOperator"] is None):
        return delegate(elements, "postfixExpression", level)
    else:
        return elements["unaryOperator"] + " " + delegate(elements, "postfixExpression", level)

@defaultExpressionParser.register(metamodel["PostfixExpression"])
def postfixExpressionParser(expression, level):
    introduce(expression, "PostfixExpression", level)
    return delegate(vars(expression), "primaryExpression", level)
    """ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    PostfixExpression:
        primaryExpression=PrimaryExpression
        ( ( "." | "->" ) propertyCall=PropertyCall )* <-------------------------------------------------------------------
    ;
    """

@defaultExpressionParser.register(metamodel["PropertyCall"])
def propertyCallParser(expression, level):
    introduce(expression, "PropertyCall", level)
    elements = vars(expression)
    result = delegate(elements, "pathName", level)
    qualifiers = elements["qualifiers"]
    if(qualifiers is not None):
        result += delegate(elements, "qualifiers", level)
    return result
    """
    PropertyCall:
        pathName=PathName
        ( timeExpression=TimeExpression )?
        ( qualifiers=Qualifiers )?
        ( propertyCallParameters=PropertyCallParameters )? <-------------------------------------------------------------------
    ;
    """

@defaultExpressionParser.register(metamodel["PathName"])
def pathNameParser(expression, level):
    introduce(expression, "PathName", level)
    return vars(expression)["names"][0]

@defaultExpressionParser.register(metamodel["Qualifiers"])
def qualifiersParser(expression, level):
    introduce(expression, "Qualifiers", level)
    result = "[ "
    result += delegate(vars(expression), "actualParameterList", level)
    result += " ]"
    return result

@defaultExpressionParser.register(metamodel["ActualParameterList"])
def actualParameterListParser(expression, level):
    introduce(expression, "ActualParameterList", level)
    content = vars(expression)["expressions"]
    result = defaultExpressionParser(content[0], level+1)
    for e in content[1:]:
        result += ", " + defaultExpressionParser(e, level+1)
    return result

@defaultExpressionParser.register(metamodel["PrimaryExpression"])
def primaryExpressionParser(expression, level):
    introduce(expression, "PrimaryExpression", level)
    elements = vars(expression)
    nestedExpression = elements["expression"]
    if(nestedExpression is not None):
        return "(" + defaultExpressionParser(nestedExpression, level+1) + ")"
    else:
        return defaultExpressionParser(extract(expression), level+1)

@defaultExpressionParser.register(metamodel["LiteralCollection"])
def literalCollectionParser(expression, level):
    introduce(expression, "LiteralCollection", level)
    elements = vars(expression)
    result = "oclWrapper_Creator(["
    collectionItems = elements["collectionItems"]
    result += defaultExpressionParser(collectionItems[0], level+1)
    for e in collectionItems[1:]:
        result += ", " + defaultExpressionParser(e, level+1)
    result += "])"
    return result

@defaultExpressionParser.register(metamodel["CollectionItem"])
def collectionItemParser(expression, level):
    introduce(expression, "CollectionItem", level)
    elements = vars(expression)
    result = delegate(elements, "startExpression", level)
    endExpression = elements["endExpression"]
    if(endExpression is not None):
        result += ".." + defaultExpressionParser(endExpression, level+1)
    return result

@defaultExpressionParser.register(metamodel["Literal"])
def literalParser(expression, level):
    introduce(expression, "Literal", level)
    return defaultExpressionParser(extract(expression), level+1)

@defaultExpressionParser.register(int)
def numberParser(expression, level):
    return str(expression)

@defaultExpressionParser.register(str)
def stringParser(expression, level):
    return "\"" + str(expression) + "\""

@defaultExpressionParser.register(metamodel["EnumLiteral"])
def enumLiteralParser(expression, level):
    introduce(expression, "EnumLiteral", level)
    names = vars(expression)["names"]
    result = names[0] + "::" + names[1]
    for e in names[2:]:
        result += ", " + e
    return result




# WHERE THE MAGIC HAPPENS

model = metamodel.model_from_file("expression.ocl")

res(0, "import sys, os\nsys.path.insert(0, os.path.join(os.path.dirname(__file__), '../Wrapper/', 'oclpyth'))\nfrom OclPyth import oclWrapper_Creator\n\n")

for expression in model.expressions:
    res(0, defaultExpressionParser(expression, 0), "\n")






logger.close()
result.close()
