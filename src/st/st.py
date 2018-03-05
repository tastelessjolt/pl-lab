from utils import inc_tabsize
class AST(object):
    pass

class Program(AST):
    def __init__(self, funclist):
        self.funclist = funclist

    def __str__(self, depth = 0):
        return 'Program {\n' + inc_tabsize('\n'.join([func.__str__() for func in self.funclist])) + '\n}'

class Func(AST):
    def __init__(self, rtype, fname, params, stlist):
        self.rtype = rtype
        self.fname = fname
        self.params = params
        self.stlist = stlist

    def __str__(self, depth = 0):
        return 'Func(' + ', '.join([self.fname, str(self.params), str(self.rtype)]) + ') {\n' + inc_tabsize('\n'.join([st.__str__() for st in self.stlist])) + '\n}'

class IfStatement(AST):
    def __init__(self, operator, condition, stlist1, stlist2=[]):
        self.operator = operator
        self.condition = condition
        self.stlist1 = stlist1
        self.stlist2 = stlist2

    def __str__(self, depth = 0):
        tmp = 'If(' + self.condition.__repr__() + ') '
        if len(self.stlist1) != 0:
            '{\n' + '\n'.join([st.__str__() for st in self.stlist1]) + '\n}'
        if len(self.stlist2) != 0:
            tmp += '\nelse {' + '\n'.join([st.__str__() for st in self.stlist2]) + '\n}'
        return tmp

class WhileStatement(AST):
    def __init__(self, operator, condition, stlist):
        self.operator = operator
        self.condition = condition
        self.stlist = stlist

    def __str__(self, depth = 0):
        tmp = 'While(' + self.condition.__repr__() + ') '
        if len(self.stlist) != 0:
            '{\n' + '\n'.join([st.__str__() for st in self.stlist]) + '\n}'
        return tmp

class ScopeBlock(AST, list):
    '''
        This describes anything of the form 'LCURLY stlist RCURLY'
    '''
    def __init__(self, stlist):
        self.stlist = stlist

    def __str__(self, depth=0):
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
    
    def __repr__(self):
        return repr(self.operator) + '(' + repr(self.operand1) + ', ' + repr(self.operand2) + ')'


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

    def __repr__(self):
        return repr(self.operator) + '(' + repr(self.operand) + ')'


class Var(AST):
    def __init__(self, label):
        self.label = label

    def __str__(self, depth=0):
        return "\t" * depth + "VAR(%s)" % self.label

    def __repr__(self):
        return self.label

class Num(AST):
    def __init__(self, val):
        self.val = val

    def __str__(self, depth=0):
        return "\t" * depth + "CONST(%d)" % self.val

    def __repr__(self):
        return str(self.val)
