from classiq.interface.generator.expressions.enums.classical_enum import ClassicalEnum


class Optimizer(ClassicalEnum):
    COBYLA = 1
    SPSA = 2
    L_BFGS_B = 3
    NELDER_MEAD = 4
    ADAM = 5
