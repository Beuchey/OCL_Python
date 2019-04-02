from textx import metamodel_from_str
from textx.model import get_metamodel

# DEFINE THE METAMODEL (GRAMMAR) AND THE MODEL TO HANDLE WITH THIS METAMODEL

# In this metamodel the "$$$$$$$" markers signal where the grammar has been simplified and needs to be completed
metamodel = metamodel_from_str("""
File:
    (expression=Expression)*
;
Expression:
    logicalExpression=LogicalExpression
;
LetExpression:
    "let" name=Name
    ( "(" formalParameterList=FormalParameterList ")" )?
    ( ":" typeSpecifier=TypeSpecifier )?
    "=" expression=Expression ";"
;
IfExpression:
    "if" ifExpression=Expression
    "then" thenExpression=Expression
    "else" elseExpression=Expression
    "endif"
;
LogicalExpression:
    relationalExpression=RelationalExpression
    ( logicalOperator=LogicalOperator
    subRelationalExpression=RelationalExpression
    )*
;
RelationalExpression:
    additiveExpression=AdditiveExpression
    ( relationalOperator=RelationalOperator
    subAdditiveExpression=AdditiveExpression
    )?
;
AdditiveExpression:
    multiplicativeExpression=MultiplicativeExpression
    ( aAddOperator=AddOperator
    subMultiplicativeExpression=MultiplicativeExpression
    )*
;
MultiplicativeExpression:
    unaryExpression=UnaryExpression
    ( multiplyOperator=MultiplyOperator
    subUnaryExpression=UnaryExpression
    )*
;
UnaryExpression:
    ( unaryOperator=UnaryOperator
     postfixExpression=PostfixExpression
     )
     | simplePostfixExpression=PostfixExpression
;
PostfixExpression:
    primaryExpression=PrimaryExpression
    ( ( "." | "->" ) propertyCall=PropertyCall )*
;
PrimaryExpression:
    literalCollection=LiteralCollection
    | literal=Literal
    | propertyCall=PropertyCall
    | "(" expression=Expression ")"
    | ifExpression=IfExpression
;
UnaryOperator:
    "-" | "not"
;
LiteralCollection:
    collectionKind=CollectionKind "{"
    ( collectionItem=CollectionItem
        ("," subCollectionItem=CollectionItem )*
    )?
    "}"
;
CollectionKind:
    "Set" | "Bag" | "Sequence" | "Collection"
;
CollectionItem:
    expression=Expression (".." subExpression=Expression )?
;
PropertyCall:
    pathName=PathName
    ( timeExpression=TimeExpression )?
    ( qualifiers=Qualifiers )?
    ( propertyCallParameters=PropertyCallParameters )?
;
Qualifiers:
    "[" actualParameterList=ActualParameterList "]"
;
PathName:
    name=Name ( "::" subName=Name )*
;
TimeExpression:
    "@" "pre"
;
ActualParameterList:
    expression=Expression ( "," subExpression=Expression )*
;
Literal:
    string=String
    | number=Number
    | enumLiteral=EnumLiteral
;
EnumLiteral:
    aName=Name "::" bName=Name ( "::" cName=Name )*
;
Name:
    body=/[a-z, A-Z, _]([a-z, A-Z, 0-9, _])*/
;
Number:
    body=NUMBER
;
String:
    body=STRING
;
PropertyCallParameters:
    "(" ( declarator=Declarator )?
    ( actualParameterList=ActualParameterList )? ")"
;
Declarator:
    name=Name ( "," subName=Name )*
    ( ":" simpleTypeSpecifier=SimpleTypeSpecifier )?
    ( ";" sName=Name ":" typeSpecifier=TypeSpecifier "="
        expression=Expression
    )?
    "|"
;
SimpleTypeSpecifier:
    pathName=PathName
;
TypeSpecifier:
    simpleTypeSpecifier=SimpleTypeSpecifier
    | collectionType=CollectionType
;
CollectionType:
    collectionKind=CollectionKind
    "(" simpleTypeSpecifier=SimpleTypeSpecifier ")"
;
LogicalOperator:
    "and" | "or" | "xor" | "implies"
;
CollectionKind:
    "Set" | "Bag" | "Sequence" | "Collection"
;
RelationalOperator:
    "=" | ">" | "<" | ">=" | "<=" | "<>"
;
AddOperator:
    "+" |  "-"
;
MultiplyOperator:
    "*" | "/"
;
UnaryOperator:
    "-" | "not"
;
FormalParameterList:
    ( name=Name ":" typeSpecifier=TypeSpecifier
    ("," subName=Name ":" subTypeSpecifier=TypeSpecifier )*
    )?
;
""")

model = metamodel.model_from_str("""
if 'hello'
then 'bambi'
else 'goodbye'
endif

if 'hello'
then 'bambi'
endif
""")







# Output tools

logger = open("log.txt","w+")
def log(*args):
    for e in args:
        logger.write(e)
    logger.write("\n")

result = open("result.txt","w+")
def res(*args):
    for e in args:
        result.write(e)
    result.write("\n")






# WHERE THE MAGIC HAPPENS



case = ""

# IF tools
ifStatement = ""
thenStatement = ""
elseStatement = ""

for exp in model.expression:
    logicalExp = exp.logicalExpression
    relationalExp = logicalExp.relationalExpression
    additiveExp = relationalExp.additiveExpression
    multiplicativeExp = additiveExp.multiplicativeExpression
    unaryExp = multiplicativeExp.unaryExpression
    simplePostfixExp = unaryExp.simplePostfixExpression
    primaryExp = simplePostfixExp.primaryExpression
    if primaryExp.literalCollection is not None:
        subcase = primaryExp.literalCollection
    elif primaryExp.literal is not None:
        subcase = primaryExp.literal
    elif primaryExp.propertyCall is not None:
        subcase = primaryExp.propertyCall
    elif primaryExp.expression is not None:
        subcase = primaryExp.expression
    elif primaryExp.ifExpression is not None:
        subcase = primaryExp.ifExpression
    log(subcase.__class__.__name__)
    if subcase.__class__.__name__ == "PropertyCall":
        subcase = subcase.pathName
    elif subcase.__class__.__name__ == "Literal":
        subcase = subcase.string
    elif subcase.__class__.__name__ == "Literal":
        subcase = subcase.string
    log("\t", subcase.__class__.__name__)
    if subcase.__class__.__name__ == "PathName":
        log("\t\tSETUP CASE : ", subcase.name.body)
        case = subcase.name.body.strip()
        if case == "endif":
            res("if ", ifStatement, ":\n\t", thenStatement)
            if(elseStatement!=""):
                res("else:\n\t", elseStatement)
            ifStatement = ""
            thenStatement = ""
            elseStatement = ""
    elif subcase.__class__.__name__ == "String":
        log("\t\tRECORDING : ", subcase.body)
        log("\t\tinside : ", case)
        if case == "if":
            ifStatement = subcase.body
        elif case == "then":
            thenStatement = subcase.body
        elif case == "else":
            elseStatement = subcase.body


logger.close()
result.close()
