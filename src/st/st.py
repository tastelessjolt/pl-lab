class AST(object):
    pass

class Program(AST):
    def __init__(self, funclist):
        self.funclist = funclist

    def __str__(self, depth = 0):
        raise NotImplementedError

class Func(AST):
    def __init__(self, rtype, fname, params, stlist):
        self.rtype = rtype
        self.fname = fname
        self.params = params
        self.stlist = stlist

    def __str__(self, depth = 0):
        raise NotImplementedError

class IfStatement(AST):
    def __init__(self, operator, condition, stlist1, stlist2=[]):
        self.operator = operator
        self.condition = condition
        self.stlist1 = stlist1
        self.stlist2 = stlist2

    def __str__(self, depth = 0):
        raise NotImplementedError

class WhileStatment(AST):
    def __init__(self, operand, condition, stlist):
        self.operator = operator
        self.condition = condition
        self.stlist = stlist

    def __str__(self, depth = 0):
        raise NotImplementedError

class Declaration(AST):
    # datatype is of class Datatype
    # varlist is list of VAR ASTs
    def __init__(self, datatype, varlist):
        self.datatype = datatype
        self.varlist = varlist

    def __str__(self, depth = 0):
        raise NotImplementedError

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

    def __str__(self, depth=0):
        return "\t" * depth + "VAR(%s)" % self.label


class Num(AST):
    def __init__(self, val):
        self.val = val

    def __str__(self, depth=0):
        return "\t" * depth + "CONST(%d)" % self.val
