from utils import inc_tabsize, DataType, IntType, FloatType, AnyType, VoidType
from utils import Operator, eprint, BooleanType, symbol_list_as_dict
from asm import *
import symtab
import symtab as symtabby


class AST(object):
    def tableEntry(self, scope=symtab.Scope.NA, parent=None):
        '''
            Basically creates a Symbol table entry
            Output: Tuple ( table_entry_or_entries, symtables_created_in_the_process ) 
        '''
        pass
    
    def get_asm(self, parser, symtab, asm):
        raise NotImplementedError

    def isNothing(self):
        return isinstance(self, Nothing)


class Nothing(AST):
    def __init__(self):
        self.type = VoidType()
    
    def __src__(self):
        return ''

    def __repr__(self):
        return ''

    def src(self):
        return ''


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

    def get_asm(self, parser, symtab, asm):
        for st in self:
            st.get_asm(parser, symtab, asm)


class Program(AST):
    def __init__(self, global_list, all_symtabs=None):
        self.global_list = global_list
        self.all_symtabs = all_symtabs
    
    def __str__(self):
        return '\n'.join([str(func) for func in self.global_list])

    def __repr__(self):
        return 'Program {\n%s\n}' % inc_tabsize('\n'.join([repr(func) for func in self.global_list]))
             

class Func(AST):
    # params are a list of type either `Symbol` or DataType's children
    def __init__(self, rtype, fname, params, stlist=None, declaration=True, lineno=-1):
        self.rtype = rtype
        self.fname = fname
        self.params = params
        self.stlist = stlist
        self.declaration = declaration
        self.lineno = lineno
    
    def __str__(self):
        if not self.declaration:
            s = '%s\n%s' % (
                ( ('%s\nPARAMS %s\nRETURNS %s' %
                   ('Function Main' if self.fname == 'main' else 'FUNCTION ' + self.fname,
                                                       symbol_list_as_dict(self.params), str(self.rtype)))),
                '\n'.join([str(stmt) if isinstance(stmt, Return) else inc_tabsize(str(stmt)) for stmt in self.stlist]))
            return s
        else:
            return ''

    def __repr__(self):
        if self.declaration:
            return 'Func %s(%s) -> %s' % (repr(self.fname), str(self.params), str(self.rtype))
        else:
            return 'Func %s(%s) -> %s {\n%s\n}' % (repr(self.fname), str(self.params), str(self.rtype),
                                            inc_tabsize('\n'.join([repr(st) for st in self.stlist])))

    def tableEntry(self, scope=symtab.Scope.NA, table_ptr=None):
        return symtab.TableEntry(self.fname, (self.rtype, self.params), scope, table_ptr, lineno=self.lineno, definition=not self.declaration)


class FuncCall(AST):
    def __init__(self, fname, params, type=DataType(), lineno=-1):
        self.fname = fname
        self.params = params
        self.type = type[0]
        self.lineno = lineno
        self.param_types = type[1]
        
        if len(params) != len(type[1]):
            eprint("Function %s expected %d arguments but provided %d at line %d" % (fname, len(type[1]), len(params), lineno))

        for i in range(len(params)):
            if params[i].type != type[1][i]:
                eprint("Function call to %s expected %s as argument number %d but given %s" % (fname, repr(type[1][i]), i, repr((params[i], params[i].type)) if issubclass(params[i].__class__, AST) else repr(params[i]) ))

    def __str__(self):
        return 'CALL %s\n(\n%s\n)\n' % (self.fname, inc_tabsize('\n,\n'.join([ '%s' % str(param) for param in self.params] )))

    def __repr__(self):
        return '%s (%s)' % ( self.fname, repr(self.params) )
    
    def src(self):
        return '%s (%s)' % ( self.fname, ", ".join([repr(param) for param in self.params]) )

    def expand(self, cfg, block):
        newParams = []
        for param in self.params:
            newParams.append(param.expand(cfg, block))
        newfuncCall = FuncCall(self.fname, newParams, (self.type, self.param_types), self.lineno)

        if isinstance(self.type, VoidType):
            block.expandedAst.append(newfuncCall)
        return newfuncCall
    
    def get_asm(self, parser, symtab, asm):
        entry = symtab.search(self.fname)
        called_symtab = entry.table_ptr
        asm.code.append(Instruction(
            comment='setting up activation record for called function'))
        for param, fparam in zip(self.params, called_symtab.parent_func.params):
            s0 = param.get_asm(parser, symtab, asm)
            entry = called_symtab.search(fparam.label)
            offset = 12 + called_symtab.width - entry.offset
            asm.code.append(Instruction(InstrOp.sw, s0, offset, Register.sp))
            asm.free_variable(param)
        asm.code.append(Instruction(InstrOp.sub, Register.sp, Register.sp,
                                    called_symtab.argument_width))
        asm.code.append(Instruction(
            InstrOp.jal, self.fname, comment='function call'))
        asm.code.append(Instruction(InstrOp.add, Register.sp, Register.sp,
                                    called_symtab.argument_width, comment='destroying activation record of called function'))
        new_reg = asm.set_register(self)
        if new_reg.is_float:
            asm.code.append(Instruction(InstrOp.move, new_reg, Register.f0,
                                    comment='using the return value of called function'))
        else:
            asm.code.append(Instruction(InstrOp.move, new_reg, Register.v1,
                                    comment='using the return value of called function'))
        return new_reg


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
    
    def get_asm(self, parser, symtab, asm):
        raise NotImplementedError


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
    
    def get_asm(self, parser, symtab, asm):
        raise NotImplementedError


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

        if isinstance(ast, Var) and ast.type.ptr_depth == 0:
            eprint("Direct use of %s type variable not allowed. Line: %d" %
                   (ast.type.basetype, lineno))

        if ast.type != type:
            eprint("The return type of the function doesn't match that of the return expression at line %d" % lineno)

    def __str__(self):
        inner = str(self.ast)
        return 'RETURN\n(\n%s\n)' % inc_tabsize(inner)
        # return ''

    def __repr__(self):
        return 'return(%s)' % str(self.ast)

    def src(self):
        return 'return %s' % self.ast.src()
    
    def expand(self, cfg, block):
        block.expandedAst.append(self)
        return self
    
    def get_asm(self, parser, symtab, asm):
        if not self.ast.isNothing():
            reg = self.ast.get_asm(parser, symtab, asm)
            if reg.is_float:
                asm.code.append(Instruction(
                    InstrOp.move, Register.f0, reg, comment='move return value to $f0'))
            else:
                asm.code.append(Instruction(InstrOp.move, Register.v1, reg, comment='move return value to $v1'))
            asm.free_variable(self.ast)


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
    def __init__(self, operator, operand1, operand2, lineno=-1, cfg=0):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.lineno = lineno

        if not cfg and isinstance(operand1, Var) and operand1.type.ptr_depth == 0:
            eprint("Direct use of %s type variable not allowed. Line: %d" % (operand1.type.basetype, lineno))
        
        if not cfg and isinstance(operand2, Var) and operand2.type.ptr_depth == 0:
            eprint("Direct use of %s type variable not allowed. Line: %d" %
                   (operand2.type.basetype, lineno))

        match = BinOp._match_types(operand1, operand2)
        if match:
            if operator._is_logical_op():
                self.type = BooleanType()
            else:
                self.type = operand1.type
        else:
            eprint("Type mismatch at line %d: %s %s %s" % (lineno, repr(operand1), repr(operator), repr(operand2)))

    @staticmethod
    def _match_types(operand1, operand2):
        return operand1.type == operand2.type

    def src(self):
        return "%s %s %s" % (self.operand1.src(), repr(self.operator), self.operand2.src())

    def __str__(self):
        s = "%s\n(\n%s\n\t,\n%s\n)" % (self.operator, inc_tabsize(str(self.operand1)), inc_tabsize(str(self.operand2)))
        return s
    
    def __repr__(self):
        return "%s(%s,%s)" % (repr(self.operator), repr(self.operand1), repr(self.operand2))

    def expand(self, cfg, block):
        if self.operator == Operator.equal:
            op2 = self.operand2.expand(cfg, block)
            if not isinstance(op2.type, VoidType):
                block.expandedAst += [BinOp(Operator.equal,
                                            self.operand1, op2, cfg=1)]
        else:
            place1 = self.operand1.expand(cfg, block)
            place2 = self.operand2.expand(cfg, block)

            if self.operator._is_arithmetic_op():
                newTmp = Var('t%d' % cfg.numtemps, type=self.operand1.type)
            elif self.operator._is_logical_op():
                newTmp = Var('t%d' % cfg.numtemps, type=BooleanType())

            cfg.numtemps += 1

            block.expandedAst += [BinOp(Operator.equal,
                                        newTmp, BinOp(self.operator, place1, place2, cfg=1), cfg=1)]
            return newTmp
    
    def get_asm(self, parser, symtab, asm):
        if self.operator._is_arithmetic_op():
            if self.operator != Operator.equal:
                reg1 = self.operand1.get_asm(parser, symtab, asm)
                reg2 = self.operand2.get_asm(parser, symtab, asm)
                if self.operator == Operator.divide:
                    if reg1.is_float:
                        new_reg = asm.set_register(self)
                        asm.code.append(Instruction(InstrOp.div, new_reg, reg1, reg2))
                        asm.free_variable(self.operand1)
                        asm.free_variable(self.operand2)
                    else:
                        asm.code.append(Instruction(InstrOp.div, reg1, reg2))
                        asm.free_variable(self.operand1)
                        asm.free_variable(self.operand2)
                        new_reg = asm.set_register(self)
                        asm.code.append(Instruction(InstrOp.mflo, new_reg))
                else:
                    new_reg = asm.set_register(self)
                    if self.operator == Operator.plus:
                        asm.code.append(Instruction(InstrOp.add, new_reg, reg1, reg2))
                    elif self.operator == Operator.minus:
                        asm.code.append(Instruction(InstrOp.sub, new_reg, reg1, reg2))
                    elif self.operator == Operator.mul:
                        asm.code.append(Instruction(InstrOp.mul, new_reg, reg1, reg2))
                    asm.free_variable(self.operand1)
                    asm.free_variable(self.operand2)
                return new_reg
            else:
                reg2 = self.operand2.get_asm(parser, symtab, asm)

                if isinstance(self.operand1, Var):
                    entry = symtab.search(self.operand1.label)
                    if entry and not entry.isFuncEntry():
                        # new_reg = asm.set_register(self.operand1)
                        # asm.code.append(Instruction(InstrOp.move, new_reg, reg2))
                        if entry.scope == symtabby.Scope.GLOBAL:
                            asm.code.append(Instruction(InstrOp.sw, reg2, "global_%s" % entry.name))
                        else:
                            asm.code.append(Instruction(InstrOp.sw, reg2, entry.offset, Register.sp))
                        asm.free_variable(self.operand2)
                        # asm.free_variable(self.operand1)
                        return
                    else:
                        new_reg = asm.get_register(self.operand1, symtab)
                        asm.code.append(Instruction(InstrOp.move, new_reg, reg2))
                        asm.free_variable(self.operand2)
                        return
                elif isinstance(self.operand1, UnaryOp):
                    reg1 = self.operand1.operand.get_asm(parser, symtab, asm)
                    asm.code.append(Instruction(InstrOp.sw, reg2, 0, reg1))
                    asm.free_variable(self.operand2)
                    asm.free_variable(self.operand1.operand)
                    return
        elif self.operator in [Operator.logical_and, Operator.logical_or]:  # logical operator
            reg1 = self.operand1.get_asm(parser, symtab, asm)
            reg2 = self.operand2.get_asm(parser, symtab, asm)
            new_reg = asm.set_register(self)

            op = {
                Operator.logical_and: InstrOp._and,
                Operator.logical_or: InstrOp._or,
            }[self.operator]
            asm.code.append(Instruction(op, new_reg, reg1, reg2))
            asm.free_variable(self.operand1)
            asm.free_variable(self.operand2)
            return new_reg
            
        else: # cmp operator
            reg1 = self.operand1.get_asm(parser, symtab, asm)
            reg2 = self.operand2.get_asm(parser, symtab, asm)
            new_reg = asm.set_register(self)
            
            mapping = { 
                Operator.cmp_eq : InstrOp.seq,
                Operator.less : InstrOp.slt,
                Operator.less_or_eq : InstrOp.sle,
                Operator.cmp_not_eq: InstrOp.sne,
            }

            op = mapping.get(self.operator, None)
            if not op:
                op = {
                    Operator.greater: InstrOp.slt,
                    Operator.greater_or_eq : InstrOp.sle,
                }[self.operator]
                tmp = reg1 
                reg1 = reg2
                reg2 = tmp
                
            if self.operand1.type.isFloat():
                if op == InstrOp.sne:
                    jump_label = 'L_CondTrue_%d' % asm.fp_j_label
                else:
                    jump_label = 'L_CondFalse_%d' % asm.fp_j_label
                end_label = 'L_CondEnd_%d' % asm.fp_j_label
                asm.fp_j_label += 1

                asm.code.append(Instruction(op, reg1, reg2))
                asm.code.append(Instruction(InstrOp.bc1f, jump_label))
                asm.code.append(Instruction(InstrOp.li, new_reg, int(op != InstrOp.sne)))
                asm.code.append(Instruction(InstrOp.j, end_label))

                asm.code.append(Label(jump_label))
                asm.code.append(Instruction(InstrOp.li, new_reg, int(op == InstrOp.sne)))
                asm.code.append(Label(end_label))
                asm.free_variable(self.operand1)
                asm.free_variable(self.operand2)
            else:
                asm.code.append(Instruction(op, new_reg, reg1, reg2))
                asm.free_variable(self.operand1)
                asm.free_variable(self.operand2)
            return new_reg


        raise Exception('Problem in BinOP Assignment')


class UnaryOp(AST):
    def __init__(self, operator, operand, lineno=-1):
        self.operator = operator
        self.operand = operand
        self.lineno = lineno
        if self.operator == Operator.ptr:
            if self.operand.type.ptr_depth == 0:
                eprint ('Extra pointer indirections: line %d: %s' % (self.lineno, repr(self.operand)))
            else: 
                self.type = type(self.operand.type)(self.operand.type.ptr_depth - 1)
        elif self.operator == Operator.ref:
            self.type = type(self.operand.type)(self.operand.type.ptr_depth + 1)
        elif self.operator == Operator.uminus:
            self.type = operand.type
        elif self.operator == Operator.logical_not:
            # No need to check operand is Boolean type. That is ensured by the parser
            self.type = operand.type

    def src(self):
        return "%s%s" % (repr(self.operator), self.operand.src())

    def __str__(self):
        s = "%s\n(\n%s\n)" % (self.operator, inc_tabsize(str(self.operand)))
        return s

    def __repr__(self):
        return "%s%s" % (repr(self.operator), repr(self.operand))

    def expand(self, cfg, block):
        if self.operator == Operator.ptr or self.operator == Operator.ref:
            return self

        place = self.operand.expand(cfg, block)

        if self.operator._is_logical_op() or self.operator._is_arithmetic_op():
            newTmp = Var('t%d' % cfg.numtemps, type=self.operand.type)
        elif self.operator == Operator.ptr:
            new_type = self.operand.type.__class__(self.operand.type.ptr_depth - 1)
            newTmp = Var('t%d' % cfg.numtemps, type=new_type)
        elif self.operator == Operator.ref:
            new_type = self.operand.type.__class__(
                self.operand.type.ptr_depth + 1)
            newTmp = Var('t%d' % cfg.numtemps, type=new_type)

        cfg.numtemps += 1

        block.expandedAst += [BinOp(Operator.equal,
                                    newTmp, UnaryOp(self.operator, place), cfg=1)]
        return newTmp
    
    def get_asm(self, parser, symtab, asm):
        if self.operator == Operator.ref:
            entry = symtab.search(self.operand.label)
            if entry and not entry.isFuncEntry():
                new_reg = asm.set_register(self)
                if entry.scope == symtabby.Scope.GLOBAL:
                    asm.code.append(Instruction(InstrOp.la, new_reg, 'global_%s' % entry.name))                   
                else:
                    asm.code.append(Instruction(InstrOp.addi, new_reg, Register.sp, entry.offset))
                return new_reg
            else:
                raise Exception('Symtab search failed')
        else:
            reg = self.operand.get_asm(parser, symtab, asm)
        if self.operator == Operator.ptr:
            new_reg = asm.set_register(self)
            asm.code.append( Instruction(InstrOp.lw, new_reg, 0, reg))
            asm.free_variable(self.operand)
            return new_reg
        elif self.operator == Operator.uminus:
            new_reg = asm.set_register(self)
            asm.code.append(Instruction(InstrOp.negu, new_reg, reg))
            asm.free_variable(self.operand)
            return new_reg
        elif self.operator == Operator.logical_not:
            new_reg = asm.set_register(self)
            asm.code.append(Instruction(InstrOp.xori, new_reg, reg, 1))
            asm.free_variable(self.operand)
            return new_reg


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
    
    def get_asm(self, parser, symtab, asm):
        entry = symtab.search(self.label)
        if entry and entry.scope == symtabby.Scope.GLOBAL:
            new_reg = asm.set_register(self)
            asm.code.append(Instruction(
                InstrOp.lw, new_reg, "global_%s" % entry.name))
            return new_reg
        else:
            return asm.get_register(self, symtab)


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
    
    def get_asm(self, parser, symtab, asm):
        new_reg = asm.set_register(self)
        asm.code.append(Instruction(InstrOp.li, new_reg, self.val))
        return new_reg
