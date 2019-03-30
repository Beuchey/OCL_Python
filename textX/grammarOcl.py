from textx import metamodel_from_str

metamodel = metamodel_from_str("""
oclFile:
    ("package" packageName=PackageName
    oclExpressions*=OclExpressions
    "endpackage")+
;

PackageName:
    packageName=/\w+/
;

OclExpressions:
    AttributeAccess | Addition
;
AttributeAccess:
    instanceName=/\w+/ '.' attributeName=/\w+/
;
Addition:
    operande1=/\w+/ '+' operande2=/\w+/
;
""")

model = metamodel.model_from_str("""
package apackage

titi.toto
titi+toto
toto.titi

endpackage
""")

methods = {
    "PackageName": lambda : "Method corresponding to PackageName",
    "AttributeAccess": lambda : "Method corresponding to AttributeAccess",
    "Addition": lambda : "Method corresponding to Addition"
}

class ExpressionNameNotFoundError(Exception):
    pass

def expressionNameNotFoundErrorRaiser():
    raise ExpressionNameNotFoundError()


def extractNameFromRepr(repr):
    return repr[repr.index(":")+1:repr.index(" ")]

result = ""

for e in model.packageName:
    print(extractNameFromRepr(repr(e)))
    elements = vars(e)
    for i in elements:
        if i[0]!='_' and i!="parent":
            print('\t', i, '\t', elements[i])

for e in model.oclExpressions:
    expressionName = extractNameFromRepr(repr(e))
    print(expressionName)
    elements = vars(e)
    for i in elements:
        if i[0]!='_' and i!="parent":
            print('\t', i, '\t', elements[i])
    result += methods.get(expressionName, expressionNameNotFoundErrorRaiser)()
