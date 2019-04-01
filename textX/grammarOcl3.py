from textx import metamodel_from_str

# DEFINE THE METAMODEL (GRAMMAR) AND THE MODEL TO HANDLE WITH THIS METAMODEL

# In this metamodel the "$$$$$$$" markers signal where the grammar has been simplified and needs to be completed
metamodel = metamodel_from_str("""
File:
    (Expression)*
;
Expression:
    LogicalExpression
;
LetExpression:
    "let" Name
    ( "(" FormalParameterList ")" )?
    ( ":" TypeSpecifier )?
    "=" Expression ";"
;
IfExpression:
    "if" Expression
    "then" Expression
    "else" Expression
    "endif"
;
LogicalExpression:
    RelationalExpression
    ( LogicalOperator
    RelationalExpression
    )*
;
RelationalExpression:
    AdditiveExpression
    ( RelationalOperator
    AdditiveExpression
    )?
;
AdditiveExpression:
    MultiplicativeExpression
    ( AddOperator
    MultiplicativeExpression
    )*
;
MultiplicativeExpression:
    UnaryExpression
    ( MultiplyOperator
    UnaryExpression
    )*
;
UnaryExpression:
    ( UnaryOperator
     PostfixExpression
     )
     | PostfixExpression
;
PostfixExpression:
    PrimaryExpression
    ( ( "." | "->" ) PropertyCall )*
;
PrimaryExpression:
    LiteralCollection
    | Literal
    | PropertyCall
    | "(" Expression ")"
    | IfExpression
;
UnaryOperator:
    "-" | "not"
;
LiteralCollection:
    CollectionKind "{"
    ( CollectionItem
        ("," CollectionItem )*
    )?
    "}"
;
CollectionKind:
    "Set" | "Bag" | "Sequence" | "Collection"
;
CollectionItem:
    Expression (".." Expression )?
;
PropertyCall:
    PathName
    ( TimeExpression )?
    ( Qualifiers )?
    ( PropertyCallParameters )?
;
Qualifiers:
    "[" ActualParameterList "]"
;
PathName:
    Name ( "::" Name )*
;
TimeExpression:
    "@" "pre"
;
ActualParameterList:
    Expression ( "," Expression )*
;
Literal:
    String
    | Number
    | EnumLiteral
;
EnumLiteral:
    Name "::" Name ( "::" Name )*
;
Name:
    /[a-z, A-Z, _]([a-z, A-Z, 0-9, _])*/
;
Number:
    NUMBER
;
String:
    STRING
;
PropertyCallParameters:
    "(" ( Declarator )?
    ( ActualParameterList )? ")"
;
Declarator:
    Name ( "," Name )*
    ( ":" SimpleTypeSpecifier )?
    ( ";" Name ":" TypeSpecifier "="
        Expression
    )?
    "|"
;
SimpleTypeSpecifier:
    PathName
;
TypeSpecifier:
    SimpleTypeSpecifier
    | CollectionType
;
CollectionType:
    CollectionKind
    "(" SimpleTypeSpecifier ")"
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
    ( Name ":" TypeSpecifier
    ("," Name ":" TypeSpecifier )*
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

def extractNameFromRepr(repr):
    return repr[repr.index(":")+1:repr.index(" ")]

result = ""

print(str(model))

print(result) # Could be printed into a file
