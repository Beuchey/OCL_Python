from textx import metamodel_from_str

metamodel = metamodel_from_str("""
oclFile:
    ("package" packageName=PackageName
    oclExpressions*=OclExpressions
    "endpackage")+
;
PackageName:
    pathName=PathName
;
OclExpressions:
    ( constraint=Constraint )*
;
Constraint:
    contextDeclaration=ContextDeclaration ( stereotype=Stereotype name=Name? ":" oclExpression=OclExpression)+
;
ContextDeclaration:
    "context" ( operationContext=OperationContext | classifierContext=ClassifierContext )
;
ClassifierContext:
    (  name=Name ":" name=Name ) | name=Name
;
OperationContext:
    name=Name "::" operationName=OperationName "(" formalParameterList=FormalParameterList ")" ( ":" returnType=ReturnType )?
;
Stereotype:
    ( "pre" | "post" | "inv" )
;
OperationName:
    name=Name | "=" | "+" | "-" | "<" | "<=" |">=" | ">" | "/" | "*" | "<>" | "implies" | "not" | "or" | "xor" | "and"
;
FormalParameterList:
    ( name=Name ":" typeSpecifier=TypeSpecifier ("," name=Name ":" typeSpecifier=TypeSpecifier )*)?
;
TypeSpecifier:
    simpleTypeSpecifier=SimpleTypeSpecifier | collectionType=CollectionType
;
CollectionType:
    collectionKind=CollectionKind "(" simpleTypeSpecifier=SimpleTypeSpecifier ")"
;
OclExpression:
    ( letExpression=LetExpression )* expression=Expression
;
ReturnType:
    typeSpecifier=TypeSpecifier
;
Expression:
    logicalExpression=LogicalExpression
;
LetExpression:
    "let" name=Name ( "(" formalParameterList=FormalParameterList ")" )? ( ":" typeSpecifier=TypeSpecifier )? "=" expression=Expression ";"
;
IfExpression:
    "if" expression=Expression "then" expression=Expression "else" expression=Expression "endif"
;
LogicalExpression:
    relationalExpression=RelationalExpression ( logicalOperator=LogicalOperator relationalExpression=RelationalExpression)*
;
RelationalExpression:
    additiveExpression=AdditiveExpression ( relationalOperator=RelationalOperator additiveExpression=AdditiveExpression)?
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
        collectionKind=CollectionKind "{" ( collectionItem=CollectionItem
-3("," collectionItem )*)?"}"collectionItem         := expression (".." expression )?propertyCall           := pathName( timeExpression )?( qualifiers )?( propertyCallParameters )?qualifiers             := "[" actualParameterList "]"declarator             := name ( "," name )*( ":" simpleTypeSpecifier )?( ";" name ":" typeSpecifier "="expression)?"|"pathName               := name ( "::" name )*timeExpression         := "@" "pre"actualParameterList    := expression ("," expression)*logicalOperator        := "and" | "or" | "xor" | "implies"collectionKind         := "Set" | "Bag" | "Sequence" | "Collection"relationalOperator     := "=" | ">" | "<" | ">=" | "<=" | "<>"addOperator            := "+" |  "-"multiplyOperator       := "*" | "/"unaryOperator          := "-" | "not"name                   := ["a"-"z", "A"-"Z", "_"]( ["a"-"z", "A"-"Z", "0"-"9", "_" ] )*number                 := ["0"-"9"] (["0"-"9"])*( "." ["0"-"9"] (["0"-"9"])* )?( ("e" | "E") ( "+" | "-" )? ["0"-"9"](["0"-"9"])*)?string                 := "'"(( ~["’","\\","\n","\r"] )|("\\"( ["n","t","b","r","f","\\","’","\""]| ["0"-"7"]( ["0"-"7"] ( ["0"-"7"] )? )?)))*"'"
""")

model = metamodel.model_from_str("""
package apackage::subpackage

titi.toto
titi+toto
toto.titi

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
    "PackageName": handlePackageName,
    "AttributeAccess": handleAttributeAccess,
    "Addition": handleAddition
}


def extractNameFromRepr(repr):
    return repr[repr.index(":")+1:repr.index(" ")]

result = ""

for e in model.packageName:
    result += methods[extractNameFromRepr(repr(e))](vars(e))

for e in model.oclExpressions:
    result += methods[extractNameFromRepr(repr(e))](vars(e))

print(result)
