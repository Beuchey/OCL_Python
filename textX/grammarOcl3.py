from textx import metamodel_from_str

# DEFINE THE METAMODEL (GRAMMAR) AND THE MODEL TO HANDLE WITH THIS METAMODEL

# In this metamodel the "$$$$$$$" markers signal where the grammar has been simplified and needs to be completed
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
    ( stereotype=Stereotype (stereoname=Name)? ":" oclExpression=Name "$$$$$$$")+
;
ContextDeclaration:
    "context"
    ( operationContext=Name "$$$$$$$" | classifierContext=Name "$$$$$$$" )
;
Stereotype:
    ( "pre" | "post" | "inv" )
;
""")

model = metamodel.model_from_str("""
package apackage::subpackage

context someContext$$$$$$$
inv someInvariant : toto$$$$$$$

context someOtherContext$$$$$$$
pre somePrecondition : titi$$$$$$$

context someDamnContext$$$$$$$
pre : tata$$$$$$$

context someOtherOtherContext$$$$$$$
post somePostcondition : tutu$$$$$$$
inv someOtherInvariant : tztz$$$$$$$

endpackage
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
    "PackageName": handlePackageName,
    "OclExpressions": handleOclExpressions,
}







# WHERE THE MAGIC HAPPENS

def extractNameFromRepr(repr):
    return repr[repr.index(":")+1:repr.index(" ")]

result = ""

for e in model.packageName:
    result += methods[extractNameFromRepr(repr(e))](vars(e))

for e in model.oclExpressions:
    result += methods[extractNameFromRepr(repr(e))](vars(e))

print(result) # Could be printed into a file
