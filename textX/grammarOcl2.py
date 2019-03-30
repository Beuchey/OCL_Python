from textx import metamodel_from_str

metamodel = metamodel_from_str("""
OclFile:
    ( "package" packageName=PackageName
    oclExpressions=OclExpressions
    "endpackage"
    )+
;
PackageName:
    pathName=PathName
;
OclExpressions:
    ( constraint=Constraint )*
;
Constraint:
    contextDeclaration=ContextDeclaration
    ( stereotype=Stereotype name=Name? ":" oclExpression=OclExpression)+
;
ContextDeclaration:
    "context"
    ( operationContext=OperationContext | classifierContext=ClassifierContext )
;
ClassifierContext:
    (  name=Name ":" name=Name )
    | name=Name
;
OperationContext:
    name=Name "::" operationName=OperationName
    "(" formalParameterList=FormalParameterList ")"
    ( ":" returnType=ReturnType )?
;
Stereotype:
    ( "pre" | "post" | "inv" )
;
OperationName:
    name=Name | "=" | "+" | "-" | "<" | "<=" |">=" | ">" | "/" | "*" | "<>" | "implies" | "not" | "or" | "xor" | "and"
;
FormalParameterList:
    ( name=Name ":" typeSpecifier=TypeSpecifier
    ("," name=Name ":" typeSpecifier=TypeSpecifier )*
    )?
;
TypeSpecifier:
    simpleTypeSpecifier=SimpleTypeSpecifier
    | collectionType=CollectionType
;
CollectionType:
    collectionKind=CollectionKind
    "(" simpleTypeSpecifier=SimpleTypeSpecifier ")"
;
OclExpression:
    ( letExpression=LetExpression )*
    expression=Expression
;
ReturnType:
    typeSpecifier=TypeSpecifier
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
    "if" expression=Expression
    "then" expression=Expression
    "else" expression=Expression
    "endif"
;
LogicalExpression:
    relationalExpression=RelationalExpression
    ( logicalOperator=LogicalOperator
    relationalExpression=RelationalExpression
    )*
;
RelationalExpression:
    additiveExpression=AdditiveExpression
    ( relationalOperator=RelationalOperator
    additiveExpression=AdditiveExpression
    )?
;
AdditiveExpression:
    multiplicativeExpression=MultiplicativeExpression ( addOperator=AddOperator multiplicativeExpression=MultiplicativeExpression)*
;
MultiplicativeExpression:
    unaryExpression=UnaryExpression ( multiplyOperator=MultiplyOperator unaryExpression=UnaryExpression)*
;
UnaryExpression:
            ( unaryOperator=UnaryOperator postfixExpression=PostfixExpression) | postfixExpression=PostfixExpression
;
PostfixExpression:
    primaryExpression=PrimaryExpression ( ( "." | "->" ) propertyCall=PropertyCall )*
;
PrimaryExpression:
    literalCollection=LiteralCollection | literal=Literal | propertyCall=PropertyCall | "(" expression=Expression ")" | ifExpression=IfExpression
;
PropertyCallParameters:
    "(" ( declarator=Declarator )? ( actualParameterList=ActualParameterList )? ")"
;
Literal:
    string=String | number=Number | enumLiteral=EnumLiteral
;
EnumLiteral:
    name=Name "::" name=Name ( "::" name=Name )*
;
SimpleTypeSpecifier:
    pathName=PathName
;
LiteralCollection:
        collectionKind=CollectionKind "{" ( collectionItem=CollectionItem ("," collectionItem=CollectionItem )* )? "}"
;
CollectionItem:
    expression=Expression (".." expression=Expression )?
;
PropertyCall:
    pathName=PathName ( timeExpression=TimeExpression )? ( qualifiers=Qualifiers )? ( propertyCallParameters=PropertyCallParameters )?
;
Qualifiers:
    "[" actualParameterList=ActualParameterList "]"
;
Declarator:
    name=Name ( "," name=Name )* ( ":" simpleTypeSpecifier=SimpleTypeSpecifier )? ( ";" name=Name ":" typeSpecifier=TypeSpecifier "=" expression=Expression)? "|"
;
PathName:
    name=Name ( "::" name=Name )*
;
TimeExpression:
    "@" "pre"
;
ActualParameterList:
        expression=Expression ( "," expression=Expression )*
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
Name:
    name=/["a"-"z", "A"-"Z", "_"] ( ["a"-"z", "A"-"Z", "0"-"9", "_" ] )*/
;
Number:
    number=/["0"-"9"] (["0"-"9"])* ( "." ["0"-"9"] (["0"-"9"])* )? ( ("e" | "E") ( "+" | "-" )? ["0"-"9"] (["0"-"9"])* )?/
;
String:
    string=/"'"(( ~["’","\\","\n","\r"] )|("\\"( ["n","t","b","r","f","\\","’","\""]| ["0"-"7"]( ["0"-"7"] ( ["0"-"7"] )? )?)))*"'"/
;
""")

model = metamodel.model_from_str("""
package xtext

context ReferenceMetamodel
inv NoAnonymousImports: alias <> null

context Action
inv NoActions : false

context ParserRule
inv CamelCaseName : name.matches('[A-Z][A-Za-z]*')

context xtext::TerminalRule
inv UpperName : name = name.toUpperCase()

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
