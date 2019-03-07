# https://github.com/pyecore/pyuml2
import pyuml2.uml as uml
import pyuml2.types as types
from pyecore.resources import ResourceSet
from pyecore.resources.resource import HttpURI
import result.OclPyth as oclpyth


rset = ResourceSet()
rset.metamodel_registry[uml.nsURI] = uml
rset.metamodel_registry[types.nsURI] = types
resource = rset.get_resource(HttpURI('https://api.genmymodel.com/projects/_eG7_QCoZEem05KmXgSfXig/xmi'))
root = resource.contents[0]

root = oclpyth.ocl_wrap(root)
print(root.oclIsKindOf(uml.Model))
