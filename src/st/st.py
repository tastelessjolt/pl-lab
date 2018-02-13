class AST(object):
    pass


class BinOp(AST):
    def __init__(self, operator, operand1, operand2):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2

    def __str__(self, depth=0):
        tab = "\t" * depth
        s = tab + "%s\n" % self.operator
        s += tab + "(\n"
        s += "%s\n" % self.operand1.__str__(depth=depth + 1)
        s += tab + "\t,\n"
        s += "%s\n" % self.operand2.__str__(depth=depth + 1)
        s += tab + ")"
        return s


class UnaryOp(AST):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __str__(self, depth=0):
        tab = "\t" * depth
        s = tab + "%s\n" % self.operator
        s += tab + "(\n"
        s += "%s\n" % self.operand.__str__(depth=depth + 1)
        s += tab + ")"
        return s


class Var(AST):
    def __init__(self, label):
        self.label = label

    def __str__(self, depth):
        return "\t" * depth + "VAR(%s)" % self.label


class Num(AST):
    def __init__(self, val):
        self.val = val

    def __str__(self, depth):
        return "\t" * depth + "CONST(%d)" % self.val
