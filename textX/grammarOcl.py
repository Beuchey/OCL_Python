from textx import metamodel_from_str

metamodel = metamodel_from_str("""
Program:
    expression*=Expression
;
Expression:
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
titi.toto
titi+toto
toto.titi
""")

methods = {
    "AttributeAccess": lambda : "Method corresponding to AttributeAccess",
    "Addition": lambda : "Method corresponding to Addition"
}

class ExpressionNameNotFoundError(Exception):
    pass

def expressionNameNotFoundErrorRaiser():
    raise ExpressionNameNotFoundError()


result = ""

for e in model.expression:
    expressionName = repr(e)
    expressionName = expressionName[expressionName.index(":")+1:expressionName.index(" ")]
    print(expressionName)
    elements = vars(e)
    for i in elements:
        if i[0]!='_' and i!="parent":
            print('\t', i, '\t', elements[i])
    result += methods.get(expressionName, expressionNameNotFoundErrorRaiser)()
