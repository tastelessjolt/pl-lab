from utils import inc_tabsize, DataType, IntType, FloatType, Operator, eprint
import symtab
class AST(object):
    def tableEntry(self, scope=symtab.Scope.NA, parent=None):
        '''
            Basically creates a Symbol table entry
            Output: Tuple ( table_entry_or_entries, symtables_created_in_the_process ) 
        '''
        pass

class DefList(AST, list):
    '''
        Used to represent list of proc-declarations and global var-declarations
    '''
    def __str__(self):
        return '\n'.join([str(st) for st in self])

    def __repr__(self):
        return '\n'.join([repr(st) for st in self])

    def __add__(self, other):
        return DefList(super(DefList, self).__add__(other))

    def src(self):
        return '\n'.join([st.src() for st in self])

class StmtList(AST, list):
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

class Program(AST):
    def __init__(self, funclist, all_symtabs=None):
        self.funclist = funclist
        self.all_symtabs = all_symtabs
    
    def __str__(self):
        return '\n'.join([str(func) for func in self.funclist])

    def __repr__(self):
        return 'Program {\n%s\n}' % inc_tabsize('\n'.join([repr(func) for func in self.funclist]))
             

class Func(AST):
    def __init__(self, rtype, fname, params, stlist=None, declaration=False, lineno=-1):
        self.rtype = rtype
        self.fname = fname
        self.params = params
        self.stlist = stlist
        self.declaration = declaration
        self.lineno = lineno
    
    def __str__(self):
        return str(self.stlist)

    def __repr__(self):
        if self.declaration:
            return 'Func %s(%s) -> %s' % (repr(self.fname), str(self.params), str(self.rtype))
        else:
            return 'Func %s(%s) -> %s {\n%s\n}' % (repr(self.fname), str(self.params), str(self.rtype),
                                            inc_tabsize('\n'.join([repr(st) for st in self.stlist])))

    def __tableEntry(self, scope=symtab.Scope.NA, parent=None):
        new_table = None
        scopes = []
        errors = []
        if not self.declaration:
            scopes = symtab.SymTab.from_stlist(self.stlist, scope=symtab.Scope.LOCAL, name=self.fname, parent=parent, params=self.params)
            if scopes:
                scopes, errors = scopes
                new_table = scopes[0]
            else:
                scopes = []
        return (symtab.TableEntry(self.fname, (self.rtype, self.params), scope, new_table, lineno=self.lineno, definition= not self.declaration), scopes, errors)

    def tableEntry(self, scope=symtab.Scope.NA, table_ptr=None):
        return symtab.TableEntry(self.fname, (self.rtype, self.params), scope, table_ptr, lineno=self.lineno, definition=not self.declaration)

class FuncCall(AST):
    def __init__(self, fname, params, type=DataType(), lineno=-1):
        self.fname = fname
        self.params = params
        self.type = type
        self.lineno = lineno

    def __str__(self):
        return str ((self.fname, self.params))

    def __repr__(self):
        return '%s (%s)' % ( self.fname, repr(self.params) )

class IfStatement(AST):
    def __init__(self, operator, condition, stlist1, stlist2=StmtList()):
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

    def __tableEntry(self, scope=symtab.Scope.NA, parent=None):
        new_table = None
        scopes = []
        scopes2 = []
        errors = []
        errors2 = []
        entries = []
        if len(self.stlist1) != 0:
            scopes = symtab.SymTab.from_stlist(self.stlist1, scope=symtab.Scope.LOCAL, name='if_cond', parent=parent)
            if scopes:
                scopes, errors = scopes
                new_table = scopes[0]
                entries.append(new_table)
            else:
                scopes = []
        if len(self.stlist2) != 0:
            scopes2 = symtab.SymTab.from_stlist(self.stlist1, scope=symtab.Scope.LOCAL, name='else', parent=parent)
            if scopes2:
                scopes2, errors2 = scopes2
                new_table = scopes2[0]
                entries.append(new_table)
            else:
                scopes2 = []
        return (symtab.TableEntry('if_cond', None, scope, new_table), scopes + scopes2, errors + errors2)


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

    def tableEntry(self, scope=symtab.Scope.NA):
        pass

class Declaration(AST):
    # varlist is list of `Symbol` ASTs
    def __init__(self, symlist):
        self.symlist = symlist

    def __str__(self):
        # AST does not have declarations
        return ''

    def __repr__(self):
        return ','.join ([ repr(sym) for sym in self.symlist ])

    def tableEntry(self, scope=symtab.Scope.NA, parent=None):
        return [sym.tableEntry(scope) for sym in self.symlist]

class Return(AST):
    # represents a return statement
    def __init__(self, ast, type=DataType(), lineno=-1):
        self.ast = ast
        self.type = type

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return 'return(%s)' % repr(self.ast)

    def src(self):
        return 'return %s' % self.ast.src()

class Symbol(AST):
    # this is only used for Declarations
    # datatype is of class Datatype
    def __init__(self, label, lineno=-1):
        self.label = label
        self.datatype = DataType()
        self.lineno = lineno

    def src(self):
        raise NotImplementedError

    def __str__(self):
        return "VAR(%s)" % self.label

    def __repr__(self):
        return str((self.label, self.datatype))

    def __add__(self, other):
        self.datatype += other
        return self

    def __eq__(self, other):
        return ((other.__class__.__bases__[0] == DataType) and (self.datatype == other)) or \
                ( (other.__class__ == self.__class__) and (self.datatype == other.datatype) )
    
    def tableEntry(self, scope=symtab.Scope.NA, parent=None):
        return symtab.TableEntry(self.label, self.datatype, scope, lineno=self.lineno)

class BinOp(AST):
    def __init__(self, operator, operand1, operand2, lineno=-1):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.type = operand1.type 
        self.lineno = lineno

    def src(self):
        return "%s %s %s" % (self.operand1.src(), repr(self.operator), self.operand2.src())

    def __str__(self):
        s = "%s\n(\n%s\n\t,\n%s\n)" % (self.operator, inc_tabsize(str(self.operand1)), inc_tabsize(str(self.operand2)))
        return s
    
    def __repr__(self):
        return "%s(%s,%s)" % (repr(self.operator), repr(self.operand1), repr(self.operand2))

    def expand(self, cfg, block):
        if self.operator == Operator.equal:
            block.expandedAst += [BinOp(Operator.equal,
                                        self.operand1, self.operand2.expand(cfg, block))]
        else:
            place1 = self.operand1.expand(cfg, block)
            place2 = self.operand2.expand(cfg, block)

            newTmp = Var('t%d' % cfg.numtemps )
            cfg.numtemps += 1

            block.expandedAst += [BinOp(Operator.equal,
                                        newTmp, BinOp(self.operator, place1, place2))]
            return newTmp

class UnaryOp(AST):
    def __init__(self, operator, operand, lineno=-1):
        self.operator = operator
        self.operand = operand
        self.lineno = lineno
        if self.operator == Operator.ptr:
            if self.operand.type.ptr_depth == 0:
                eprint ('Extra pointer indirections: line %d: %s' % (self.lineno, repr(self.operand)))
                raise SyntaxError
            else: 
                self.type = type(self.operand.type)(self.operand.type.ptr_depth - 1)
        elif self.operator == Operator.ref:
            self.type = type(self.operand.type)(self.operand.type.ptr_depth + 1)
        elif self.operator == Operator.uminus:
        #     if self.operand.type.ptr_depth > 0:
        #         eprint ('Unary Minus operator on pointer: line %d: %s' % (self.lineno, repr(self.operand)) )
        #         raise SyntaxError
            self.type = self.operand.type

    def src(self):
        return "%s%s" % (repr(self.operator), self.operand.src())

    def __str__(self):
        s = "%s\n(\n\t%s\n)" % (self.operator, str(self.operand))
        return s

    def __repr__(self):
        return "%s%s" % (repr(self.operator), repr(self.operand))

    def expand(self, cfg, block):
        if self.operator == Operator.logical_not or self.operator == Operator.uminus:
            place = self.operand.expand(cfg, block)

            newTmp = Var('t%d' % cfg.numtemps)
            cfg.numtemps += 1

            block.expandedAst += [BinOp(Operator.equal,
                                        newTmp, UnaryOp(self.operator, place))]
        else:
            newTmp = self
        return newTmp
        

class Var(AST):    
    def __init__(self, label, type=DataType(), lineno=-1):
        self.label = label
        self.type = type
        self.lineno = lineno

    def src(self):
        return self.label

    def __str__(self):
        return "VAR(%s)" % self.label

    def __repr__(self):
        return self.label

    def expand(self, cfg, block):
        return self

class Num(AST):
    def __init__(self, val, lineno=-1):
        self.val = val
        self.lineno = lineno
        if type(val) == int:
            self.type = IntType(0)
        elif type(val) == float:
            self.type = FloatType(0)

    def src(self):
        return str(self.val)

    def __str__(self):
        return "CONST(%d)" % self.val

    def __repr__(self):
        return str(self.val)

    def expand(self, cfg, block):
        return self
