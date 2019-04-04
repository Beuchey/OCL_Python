from functools import singledispatch
from textx import metamodel_from_file


oclmm = metamodel_from_file('textX/ocl.tx')


@singledispatch
def base(arg, *args, **kwargs):
    print("Default", arg)


@base.register(oclmm["LogicalExpression"])
def multiplicative(expression, *args, **kwargs):
    print("Logical")
    base(expression.left)
    if expression.operator != []:
        base(expression.right)


@base.register(oclmm["RelationalExpression"])
def multiplicative(expression, *args, **kwargs):
    print("relational")
    base(expression.left)
    if expression.operator != []:
        base(expression.right)


@base.register(oclmm["AdditiveExpression"])
def multiplicative(expression, *args, **kwargs):
    print("additive")
    base(expression.left)
    if expression.operator != []:
        for operator, subexp in zip(expression.operator, expression.right):
            print("ok", operator, subexp)
            base(subexp)


@base.register(oclmm["MultiplicativeExpression"])
def multiplicative(arg, *args, **kwargs):
    print("multiplicative", arg)



model = oclmm.model_from_file('textX/expression.ocl')

base(model)
