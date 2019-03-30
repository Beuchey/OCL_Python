from textx import metamodel_from_str

grammar = """
HelloWorldModel:
  'hello' to_greet+=Who[',']
;

Who:
  name = /[^,]*/
;
"""

grammar2="""
Program:
    expression*=Expression
;

Expression:
    AttributeAccess | Addition
;

AttributeAccess:
    instanceName=/\w+/ '.' attributeName=/\w+/
;

Addition:
    operande1=/\w+/ '+' operande2=/\w+/
;

"""

mm = metamodel_from_str(grammar2)

# Meta-model knows how to parse and instantiate models.
model = mm.model_from_str("""
    titi.toto
    titi+toto
    toto.titi
""")

for e in model.expression :
    print(e)
