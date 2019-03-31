from textx import metamodel_from_str

metamodel = metamodel_from_str("""
oclFile:
    ("package" packageName=PackageName
    oclExpressions=OclExpressions
    "endpackage")+
;
PackageName:
    body=Path
;
Path:
    pathname=Name ( "::" pathsubname=Name )*
;
Name:
    body=/[a-z, A-Z, _]([a-z, A-Z, 0-9, _])*/
;
OclExpressions:
    ( constraint=Constraint )*
;
Constraint:
    contextDeclaration=ContextDeclaration
;
ContextDeclaration:
    "context" body=Name
    ( stereotype=Stereotype stereoname=Name)+
;
Stereotype:
    ( "pre" | "post" | "inv" )
;
""")

model = metamodel.model_from_str("""
package apackage::subpackage

context someContext
inv someInvariant

context someOtherContext
pre somePrecondition

context someOtherOtherContext
post somePostcondition
inv someOtherInvariant

endpackage
""")

def handlePackageName(elements):
    packageComposition = vars(elements["body"])
    packageName = packageComposition["pathname"]
    packageSubname = packageComposition["pathsubname"]
    return "Context : PackageName\n\t" + "Package name = " + packageName.body + "\tPackage subname = " + packageSubname[0].body + "\n"

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

print(result)
