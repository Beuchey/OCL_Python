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

expressions = {
    "AttributeAccess": {"rule": "instanceName=/\w+/ '.' attributeName=/\w+/", "method": lambda : print("Method corresponding to AttributeAccess")},
    "Addition": {"rule":"operande1=/\w+/ '+' operande2=/\w+/", "method": lambda : print("Method corresponding to Addition")}
}

grammar = "Program:\n\texpression*=Expression\n;\n\nExpression:\n\t"

for e in expressions:
    grammar += e + ' | '

grammar += "\n;"

for e in expressions:
    grammar += "\n\n" + e + ':\n\t' + expressions[e]["rule"]

print(grammar)



metamodel = metamodel_from_str(grammar)

model = metamodel.model_from_str("""
titi.toto
titi+toto
toto.titi
""")





expressionNameNotFoundExcpetionRaiser = lambda : print("ExpressionNameNotFoundExcpetion raised")

for e in model.expression:
    expressionName = repr(e)
    expressionName = expressionName[expressionName.index(":")+1:expressionName.index(" ")]
    print(expressionName)
    elements = vars(e)
    for i in elements:
        if i[0]!='_' and i!="parent":
            print('\t', i, '\t', elements[i])
    expressions.get(expressionName, expressionNameNotFoundExcpetionRaiser)["method"]()
