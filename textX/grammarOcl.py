from textx import metamodel_from_str

expressions = {
    "AttributeAccess": (
            "instanceName=/\w+/ '.' attributeName=/\w+/",
            lambda : "Method corresponding to AttributeAccess"
    ),
    "Addition": (
            "operande1=/\w+/ '+' operande2=/\w+/",
            lambda : "Method corresponding to Addition"
    )
}



def createGrammar(expressions):

    grammar = "Program:\n\texpression*=Expression\n;\n\nExpression:\n\t"

    for e in expressions:
        grammar += e + ' | '

    grammar = grammar[:len(grammar)-2]

    grammar += "\n;"

    for e in expressions:
        grammar += "\n\n" + e + ':\n\t' + expressions[e][0] + "\n;"

    return grammar






model = metamodel_from_str(createGrammar(expressions)).model_from_str("""
titi.toto
titi+toto
toto.titi
""")







expressionNameNotFoundExcpetionRaiser = lambda : "ExpressionNameNotFoundExcpetion raised"






res = ""

for e in model.expression:
    expressionName = repr(e)
    expressionName = expressionName[expressionName.index(":")+1:expressionName.index(" ")]
    print(expressionName)
    elements = vars(e)
    for i in elements:
        if i[0]!='_' and i!="parent":
            print('\t', i, '\t', elements[i])
    res += expressions.get(expressionName, expressionNameNotFoundExcpetionRaiser)[1]()



print(res)
