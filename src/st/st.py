from utils import inc_tabsize
class AST(object):
    pass

class Program(AST):
    def __init__(self, funclist):
        self.funclist = funclist
    
    def __str__(self):
        return '\n'.join([str(func) for func in self.funclist])

    def __repr__(self):
        return 'Program {\n%s\n}' % inc_tabsize('\n'.join([repr(func) for func in self.funclist]))

class Func(AST):
    def __init__(self, rtype, fname, params, stlist):
        self.rtype = rtype
        self.fname = fname
        self.params = params
        self.stlist = stlist
    
    def __str__(self):
        s = ''
        for st in self.stlist:
            if isinstance(st, list):
                s += '\n'.join([str(i) for i in st]) + "\n"
            elif not isinstance(st, Declaration):
                s += '\n' + str(st) + "\n"
        return s

    def __repr__(self):
        return 'Func(%s) {\n%s\n}' % (', '.join([self.fname, str(self.params), str(self.rtype)]),
                                        inc_tabsize('\n'.join([repr(st) for st in self.stlist])))

class IfStatement(AST):
    def __init__(self, operator, condition, stlist1, stlist2=[]):
        self.operator = operator
        self.condition = condition
        self.stlist1 = stlist1
        self.stlist2 = stlist2

    def __str__(self):
        s = 'IF(\n%s\n\t,\n' % inc_tabsize(str(self.condition))

        # Statements in the if block
        if len(self.stlist1) != 0:
            for st in self.stlist1:
                if isinstance(st, list):
                    s += '%s\n' % inc_tabsize('\n'.join([str(i) for i in st]))
                else:
                    s += '%s\n' % inc_tabsize(str(st))
        # Statements in else block
        if len(self.stlist2) != 0:
            for st in self.stlist2:
                if isinstance(st, list):
                    s += '%s\n' % inc_tabsize('\n'.join([str(i) for i in st]))
                else:
                    s += '%s\n' % inc_tabsize(str(st))

        s += '\n)'
        return s

    def __repr__(self):
        s = 'If(' + str(self.condition) + ') '
        if len(self.stlist1) != 0:
            s += '{\n' + inc_tabsize('\n'.join([repr(st) for st in self.stlist1])) + '\n}'
        if len(self.stlist2) != 0:
            s += '\nelse {\n' + inc_tabsize('\n'.join([repr(st) for st in self.stlist2])) + '\n}'
        return s

class WhileStatement(AST):
    def __init__(self, operator, condition, stlist):
        self.operator = operator
        self.condition = condition
        self.stlist = stlist

    def __str__(self):
        s = 'WHILE(\n%s\n\t,\n' % inc_tabsize(str(self.condition))

        # Statements inside while
        if len(self.stlist) != 0:
            for st in self.stlist:
                if isinstance(st, list):
                    s += '%s\n' % inc_tabsize('\n'.join([str(i) for i in st]))
                else:
                    s += '%s\n' % inc_tabsize(str(st))
        
        s += '\n)'
        return s

    def __repr__(self):
        s = 'While(' + repr(self.condition) + ') '
        if len(self.stlist) != 0:
            s += '{\n' + inc_tabsize('\n'.join([repr(st) for st in self.stlist])) + '\n}'
        return s

class ScopeBlock(AST):
    '''
        This describes anything of the form 'LCURLY stlist RCURLY'
    '''
    def __init__(self, stlist):
        self.stlist = stlist

    def __str__(self):
        return '\n'.join([str(st) for st in self.stlist])

    def __repr__(self):
        return '\n'.join([repr(st) for st in self.stlist])

class Declaration(AST):
    # varlist is list of Symbol ASTs
    def __init__(self, symlist):
        self.symlist = symlist

    def __str__(self):
        # AST does not have declarations
        return ''

    def __repr__(self):
        return ','.join ([ repr(sym) for sym in self.symlist ])

class Symbol(AST):
    # datatype is of class Datatype
    def __init__(self, label, datatype=0):
        self.label = label
        self.datatype = datatype

    def src(self):
        raise NotImplementedError

    def __str__(self):
        return "VAR(%s)" % self.label

    def __repr__(self):
        return str((self.label, self.datatype))

    def __add__(self, other):
        self.datatype += other
        return self

class BinOp(AST):
    def __init__(self, operator, operand1, operand2):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2

    def src(self):
        return "%s %s %s" % (self.operand1.src(), repr(self.operator), self.operand2.src())

    def __str__(self):
        s = "%s\n(\n%s\n\t,\n%s\n)" % (self.operator, inc_tabsize(str(self.operand1)), inc_tabsize(str(self.operand2)))
        return s
    
    def __repr__(self):
        return "%s(%s,%s)" % (repr(self.operator), repr(self.operand1), repr(self.operand2))


class UnaryOp(AST):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def src(self):
        return "%s%s" % (repr(self.operator), self.operand.src())

    def __str__(self):
        s = "%s\n(\n\t%s\n)" % (self.operator, str(self.operand))
        return s

    def __repr__(self):
        return "%s%s" % (repr(self.operator), repr(self.operand))


class Var(AST):    
    def __init__(self, label):
        self.label = label

    def src(self):
        return self.label

    def __str__(self):
        return "VAR(%s)" % self.label

    def __repr__(self):
        return self.label

class Num(AST):
    def __init__(self, val):
        self.val = val

    def src(self):
        return str(self.val)

    def __str__(self):
        return "CONST(%d)" % self.val

    def __repr__(self):
        return str(self.val)
