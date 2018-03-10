from utils import inc_tabsize, DataType, Operator
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
        return str(self.stlist)

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
        inner = '%s\n' % str(self.condition)

        if len(self.stlist1) != 0:
            inner += ',\n'
            inner += str(self.stlist1)

        if len(self.stlist2) != 0:
            inner += '\n,\n'
            inner += str(self.stlist2)

        return 'IF\n(\n%s\n)' % inc_tabsize(inner)

    def __repr__(self):
        s = 'If(' + repr(self.condition) + ') '
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
        inner = '%s\n' % str(self.condition)

        if len(self.stlist) != 0:
            inner += ',\n'
            inner += str(self.stlist)

        return 'WHILE\n(\n%s\n)' % inc_tabsize(inner)

    def __repr__(self):
        s = 'While(' + repr(self.condition) + ') '
        if len(self.stlist) != 0:
            s += '{\n' + inc_tabsize('\n'.join([repr(st) for st in self.stlist])) + '\n}'
        return s

class StmtList(list):
    '''
        Used to represent list of statements
    '''
    def __str__(self):
        return '\n'.join([str(st) for st in self])

    def __repr__(self):
        return '\n'.join([repr(st) for st in self])

    def __add__(self, other):
        return StmtList(super(StmtList, self).__add__(other))

    def src(self):
        return '\n'.join([st.src() for st in self])

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
    def __init__(self, label):
        self.label = label
        self.datatype = DataType()

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

    def expand(self, cfg, block):
        place1 = self.operand1.expand(cfg, block)
        place2 = self.operand2.expand(cfg, block)

        newTmp = Var('t%d' % cfg.numtemps )
        cfg.numtemps += 1

        block.expandedAst += [BinOp(Operator.equal,
                                    newTmp, BinOp(self.operator, place1, place2))]
        return newTmp


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

    def expand(self, cfg, block):
        if self.operator == Operator.logical_not:
            place = self.operand.expand(cfg, block)

            newTmp = Var('t%d' % cfg.numtemps)
            cfg.numtemps += 1

            block.expandedAst += [BinOp(Operator.equal,
                                        newTmp, UnaryOp(self.operator, place))]
        else:
            newTmp = self
        return newTmp
        

class Var(AST):    
    def __init__(self, label):
        self.label = label

    def src(self):
        return self.label

    def __str__(self):
        return "VAR(%s)" % self.label

    def __repr__(self):
        return self.label

    def expand(self, cfg, block):
        return self

class Num(AST):
    def __init__(self, val):
        self.val = val

    def src(self):
        return str(self.val)

    def __str__(self):
        return "CONST(%d)" % self.val

    def __repr__(self):
        return str(self.val)

    def expand(self, cfg, block):
        return self
