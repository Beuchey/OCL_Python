from textx import metamodel_from_str

metamodel = metamodel_from_str("""
oclFile:
    ("package" packageName=PackageName
    oclExpressions*=OclExpressions
    "endpackage")+
;
PackageName:
    packageName=Path
;
Path:
    name=Name ( "::" subname=Name )*
;
Name:
    name=/[a-z, A-Z, _]([a-z, A-Z, 0-9, _])*/
;
OclExpressions:
    AttributeAccess | Addition
;
AttributeAccess:
    instanceName=/\w+/ '.' attributeName=/\w+/
;
Addition:
    operand1=/\w+/ '+' operand2=/\w+/
;
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
