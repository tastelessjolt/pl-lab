class AST(object):
    pass


class BinOp(AST):
    def __init__(self, operator, operand1, operand2):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2

    def __str__(self):
        return "%s %s %s" % (self.operand1, self.operator, self.operand2)


class UnaryOp(AST):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __str__(AST):
        return "%s %s" % (self.operator, self.operand)


class Var(AST):
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return self.label


class Num(AST):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)
