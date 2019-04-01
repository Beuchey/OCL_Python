from textx import metamodel_from_str

metamodel = metamodel_from_str("""
OclFile:
    ( "package" PackageName
    OclExpressions
    "endpackage"
    )+
;
PackageName:
    PathName
;
OclExpressions:
    ( Constraint )*
;
Constraint:
    ContextDeclaration
    ( Stereotype Name? ":" OclExpression)+
;
ContextDeclaration:
    "context"
    ( OperationContext | ClassifierContext )
;
ClassifierContext:
    (  Name ":" Name )
    | Name
;
OperationContext:
    Name "::" OperationName
    "(" FormalParameterList ")"
    ( ":" ReturnType )?
;
Stereotype:
    ( "pre" | "post" | "inv" )
;
OperationName:
    Name | " | "+" | "-" | "<" | " " | ">" | "/" | "*" | "<>" | "implies" | "not" | "or" | "xor" | "and"
;
FormalParameterList:
    ( Name ":" TypeSpecifier
    ("," Name ":" TypeSpecifier )*
    )?
;
TypeSpecifier:
    SimpleTypeSpecifier
    | CollectionType
;
CollectionType:
    CollectionKind
    "(" SimpleTypeSpecifier ")"
;
OclExpression:
    ( LetExpression )*
    Expression
;
ReturnType:
    TypeSpecifier
;
Expression:
    LogicalExpression
;
LetExpression:
    "let" Name
    ( "(" FormalParameterList ")" )?
    ( ":" TypeSpecifier )?
    " Expression ";"
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
PropertyCallParameters:
    "(" ( Declarator )?
    ( ActualParameterList )? ")"
;
Literal:
    String
    | Number
    | EnumLiteral
;
EnumLiteral:
    Name "::" Name ( "::" Name )*
;
SimpleTypeSpecifier:
    PathName
;
LiteralCollection:
    CollectionKind "{"
    ( CollectionItem
        ("," CollectionItem )*
    )?
    "}"
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
Declarator:
    Name ( "," Name )*
    ( ":" SimpleTypeSpecifier )?
    ( ";" Name ":" TypeSpecifier "
        Expression
    )?
    "|"
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
LogicalOperator:
    "and" | "or" | "xor" | "implies"
;
CollectionKind:
    "Set" | "Bag" | "Sequence" | "Collection"
;
RelationalOperator:
    " | ">" | "<" | " | " | "<>"
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
Name:
    /[a-z, A-Z, _]([a-z, A-Z, 0-9, _])*/
;
Number:
    NUMBER
;
String:
    STRING
;
""")

model = metamodel.model_from_str("""
package xtext::sss

context Action
inv NoActions : false

endpackage
""")

def handlePackageName(elements):
    packageComposition = vars(elements["packageName"])
    packageName = packageComposition["name"]
    packageSubname = packageComposition["subname"]
    return "Context : PackageName\n\t" + "Package name = " + packageName.name + "\tPackage subname = " + packageSubname[0].name + "\n"

def handleAttributeAccess(elements):
    return "Context : AttributeAccess\n\t" + "Instance name = " + elements["instanceName"] + "\tAttribute name = " + elements["attributeName"] + "\n"

def handleAddition(elements):
    return "Context : Addition\n\t" + "Operand 1 = " + elements["operand1"] + "\tOperand 2 = " + elements["operand2"] + "\n"

methods = {
}


def extractNameFromRepr(repr):
    return repr[repr.index(":")+1:repr.index(" ")]

result = ""

for e in model.packageName:
    result += methods[extractNameFromRepr(repr(e))](vars(e))

for e in model.oclExpressions:
    result += extractNameFromRepr(repr(e)) + '\n'
    #result += methods[extractNameFromRepr(repr(e))](vars(e))

print(result)
