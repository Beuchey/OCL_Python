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
     | otherPostfixExpression=PostfixExpression
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
""")




# MECHANISM TO HANDLE EVERY PART OF THE MODEL ACCORDING TO THE CORRESPONDING METAMODEL

def handlePackageName(elements):
    packageComposition = vars(elements["body"])
    packageName = packageComposition["pathname"]
    packageSubname = packageComposition["pathsubname"]
    return "Handling : PackageName\n\t" + "Package name = " + packageName.body + "\tPackage subname = " + packageSubname[0].body + "\n"

def handleOclExpressions(elements):
    return "Handling : OCL expressions\n\t..."

methods = {
    "Expression": handleOclExpressions,
}







# WHERE THE MAGIC HAPPENS



for exp in model.expression:
    print(exp.__class__.__name__)
    logicalExp = exp.logicalExpression
    relationalExp = logicalExp.relationalExpression
    additiveExp = relationalExp.additiveExpression
    multiplicativeExp = additiveExp.multiplicativeExpression
    unaryExp = multiplicativeExp.unaryExpression
    otherPostfixExp = unaryExp.otherPostfixExpression
    primaryExp = otherPostfixExp.primaryExpression
    print('\t', vars(primaryExp))
