from textx import metamodel_from_str

grammar = """
Expression:
    access+=AttributeAccess
;

AttributeAccess: instance=/\w+/ '.' att_name=STRING
;

"""

mm = metamodel_from_str(grammar)

# Meta-model knows how to parse and instantiate models.
model = mm.model_from_str("""
    toto."titi"
""")

print(model.access[0].att_name)
