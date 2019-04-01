from textx import metamodel_from_str
from textx.model import get_metamodel

# DEFINE THE METAMODEL (GRAMMAR) AND THE MODEL TO HANDLE WITH THIS METAMODEL

# In this metamodel the "$$$$$$$" markers signal where the grammar has been simplified and needs to be completed
metamodel = metamodel_from_str("""
File:
    (Expression)*
;
Expression:
    a=LogicalExpression
;
LetExpression:
    "let" a=Name
    ( "(" b=FormalParameterList ")" )?
    ( ":" c=TypeSpecifier )?
    "=" d=Expression ";"
;
IfExpression:
    "if" a=Expression
    "then" b=Expression
    "else" c=Expression
    "endif"
;
LogicalExpression:
    a=RelationalExpression
    ( b=LogicalOperator
    c=RelationalExpression
    )*
;
RelationalExpression:
    a=AdditiveExpression
    ( b=RelationalOperator
    c=AdditiveExpression
    )?
;
AdditiveExpression:
    a=MultiplicativeExpression
    ( b=AddOperator
    c=MultiplicativeExpression
    )*
;
MultiplicativeExpression:
    a=UnaryExpression
    ( b=MultiplyOperator
    c=UnaryExpression
    )*
;
UnaryExpression:
    ( a=UnaryOperator
     b=PostfixExpression
     )
     | c=PostfixExpression
;
PostfixExpression:
    a=PrimaryExpression
    ( ( "." | "->" ) b=PropertyCall )*
;
PrimaryExpression:
    a=LiteralCollection
    | b=Literal
    | c=PropertyCall
    | "(" d=Expression ")"
    | e=IfExpression
;
UnaryOperator:
    "-" | "not"
;
LiteralCollection:
    a=CollectionKind "{"
    ( b=CollectionItem
        ("," c=CollectionItem )*
    )?
    "}"
;
CollectionKind:
    "Set" | "Bag" | "Sequence" | "Collection"
;
CollectionItem:
    a=Expression (".." b=Expression )?
;
PropertyCall:
    a=PathName
    ( b=TimeExpression )?
    ( c=Qualifiers )?
    ( d=PropertyCallParameters )?
;
Qualifiers:
    "[" a=ActualParameterList "]"
;
PathName:
    a=Name ( "::" b=Name )*
;
TimeExpression:
    "@" "pre"
;
ActualParameterList:
    a=Expression ( "," b=Expression )*
;
Literal:
    a=String
    | b=Number
    | c=EnumLiteral
;
EnumLiteral:
    a=Name "::" b=Name ( "::" c=Name )*
;
Name:
    a=/[a-z, A-Z, _]([a-z, A-Z, 0-9, _])*/
;
Number:
    a=NUMBER
;
String:
    a=STRING
;
PropertyCallParameters:
    "(" ( a=Declarator )?
    ( b=ActualParameterList )? ")"
;
Declarator:
    a=Name ( "," b=Name )*
    ( ":" c=SimpleTypeSpecifier )?
    ( ";" d=Name ":" e=TypeSpecifier "="
        f=Expression
    )?
    "|"
;
SimpleTypeSpecifier:
    a=PathName
;
TypeSpecifier:
    a=SimpleTypeSpecifier
    | b=CollectionType
;
CollectionType:
    a=CollectionKind
    "(" b=SimpleTypeSpecifier ")"
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
    ( a=Name ":" b=TypeSpecifier
    ("," c=Name ":" d=TypeSpecifier )*
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

print(str(vars(vars(vars(vars(vars(vars(vars(vars(vars(vars(vars(model)["a"])["a"])["a"])["a"])["a"])["c"])["a"])["c"])["a"])["a"])["a"]))
