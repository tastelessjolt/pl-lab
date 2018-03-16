import ply.yacc as yacc
from enum import Enum
from lex import *
from st import *
from utils import *
from symtab import *
import operator

'''
Parsing with yacc
'''

class Stats:
    '''
        t = (
            0,  # no of variables
            0,  # no of pointers
            0  # no of assignments
        )
    '''

    def __init__(self, t):
        self.t = t

    def __add__(self, other):
        return Stats(tuple(map(operator.add, self.t, other.t)))

class YaccOutput(Enum):
    STATS = 0
    AST = 1

class APLYacc(object):
    reserved = APLLexer.reserved
    tokens = APLLexer.tokens

    precedence = [
        ('left', 'LOGICAL_OR'),
        ('left', 'LOGICAL_AND'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'STR', 'DIVIDE'),
        ('right', 'UMINUS', 'DEREF', 'REF', 'LOGICAL_NOT'),
        ('left', 'LESS_THAN', 'GREATER_THAN', 'LESS_EQUAL', 'GREATER_EQUAL'),
        ('left', 'DOUBLE_EQUAL', 'NOT_EQUAL'),
    ]

    def __init__(self, output=YaccOutput.AST, write_tables=True, isSymtab=True):
        self.output = output
        self.write_tables = write_tables
        self.isSymtab = isSymtab
        if isSymtab and output == YaccOutput.AST:
            self.symtab = SymTab()

#######################################################################
######################### Grammar Starts Here #########################
#######################################################################

    start = 'program'
    def p_program(self, p):
        '''
            program : global_list
        '''
        if self.output == YaccOutput.STATS:
            p[0] = p[1]
        elif self.output == YaccOutput.AST:
            p[0] = Program([p[1]])
            for glob in p[1]:
                if isinstance(glob, Func):
                    self.symtab.insert(TableEntry(glob.fname, (glob.rtype, glob.params), Scope.GLOBAL))
                elif isinstance(glob, Declaration):
                    for var in glob.symlist:
                        self.symtab.insert(TableEntry(var.label, var.datatype, Scope.GLOBAL))

    def p_epsilon(self, p):
        '''
            epsilon :
        '''
        pass

    def p_global_list(self, p):
        '''
            global_list : procedure_dec SEMICOLON global_list
                        | declaration SEMICOLON global_list
                        | procedure_def global_list
                        | main global_list
                        | epsilon
        '''
        if self.output == YaccOutput.AST:
            try: 
                p[0] = DefList([p[1]]) + p[3]
            except:
                try:
                    p[0] = DefList([p[1]]) + p[2]
                except:
                    p[0] = DefList()

    def p_procedure_def(self, p):
        '''
            procedure_def : type STR var LPAREN arglist RPAREN block
        '''
        if self.output == YaccOutput.AST:
            p[0] = Func(p[1](p[3].datatype), p[3].label, p[5], p[7].stlist)
                
    def p_procedure_def_empty(self, p):
        ''' 
            procedure_def : type STR var LPAREN RPAREN block
        '''
        if self.output == YaccOutput.AST:
            p[0] = Func(p[1](p[3].datatype), p[3].label, [], p[6].stlist)


    def p_procedure_dec(self, p):
        '''
            procedure_dec : type STR var LPAREN proto_arglist RPAREN
                            | type STR var LPAREN arglist RPAREN
        '''
        if self.output == YaccOutput.AST:
            p[0] = Func(p[1](p[3].datatype), p[3].label, p[5], declaration=True)
                

    def p_procedure_dec_empty(self, p):
        '''
            procedure_dec : type STR var LPAREN RPAREN
        '''
        if self.output == YaccOutput.AST:
            p[0] = Func(p[1](p[3].datatype), p[3].label, [], declaration=True)

    def p_proto_arglist(self, p):
        '''
            proto_arglist : d_type proto_arglist_helper
                            | d_type arglist_helper
        '''
        if self.output == YaccOutput.AST:
            p[0] = [p[1]] + p[2]

    def p_proto_arglist_var(self, p):
        '''
            proto_arglist : type STR var proto_arglist_helper
        '''
        if self.output == YaccOutput.AST:
            p[3].datatype = p[1](p[3].datatype)
            p[0] = [p[3]] + p[4]

    def p_proto_arglist_helper(self, p):
        '''
            proto_arglist_helper : COMMA d_type proto_arglist_helper
                                | COMMA d_type arglist_helper
        '''
        if self.output == YaccOutput.AST:
            p[0] = [p[2]] + p[3]

    def p_proto_arglist_helper_transition(self, p):
        '''
            proto_arglist_helper : COMMA type STR var proto_arglist_helper
        '''
        if self.output == YaccOutput.AST:
            p[4].datatype = p[2](p[4].datatype)
            p[0] = [p[4]] + p[5]

    def p_arglist(self, p):
        '''
            arglist : type STR var arglist_helper
        '''
        if self.output == YaccOutput.AST:
            p[3].datatype = p[1](p[3].datatype)
            p[0] = [p[3]] + p[4]
    
    def p_arglist_helper(self, p):
        '''
            arglist_helper : COMMA type STR var arglist_helper
        '''
        if self.output == YaccOutput.AST:
            p[4].datatype = p[2](p[4].datatype)
            p[0] = [p[4]] + p[5] 
                

    def p_arglist_helper_empty(self, p):
        '''
            arglist_helper : epsilon
        '''
        if self.output == YaccOutput.AST:
            p[0] = []

    def p_derived_type(self, p):
        '''
            d_type : type STR str
        '''
        if self.output == YaccOutput.AST:
            p[0] = p[1](p[3] + 1)

    def p_str(self, p):
        '''
            str : STR str %prec DEREF
                | epsilon
        '''
        if self.output == YaccOutput.AST:
            try: 
                p[0] = p[2] + 1
            except:
                p[0] = 0


    def p_main(self, p):
        '''
            main : VOID MAIN LPAREN RPAREN block
        '''
        if self.output == YaccOutput.STATS:
            p[0] = p[6]
        elif self.output == YaccOutput.AST:
            p[0] = Func(VoidType(), 'main', [], p[5].stlist)

    def p_statements(self, p):
        '''
            stlist : stmt stlist
                    | epsilon
        '''
        if self.output == YaccOutput.STATS:
            try:
                p[0] = p[1] + p[2]
            except:
                p[0] = Stats((0, 0, 0))
        elif self.output == YaccOutput.AST:
            try:
                p[0] = StmtList([p[1]]) + p[2]
            except:
                p[0] = StmtList()

#######################################################################3

    def p_stmt(self, p):
        '''
            stmt : matched_stmt
                | unmatched_stmt
        '''
        if self.output == YaccOutput.STATS:
            p[0] = p[1]
        elif self.output == YaccOutput.AST:
            p[0] = p[1]

    def p_matched_stmt(self, p):
        '''
            matched_stmt : IF LPAREN condition RPAREN matched_stmt ELSE matched_stmt
                        | WHILE LPAREN condition RPAREN matched_stmt
                        | other
        '''
        if self.output == YaccOutput.STATS:
            if p[1] == 'if':
                p[0] = p[5] + p[7]
            elif p[1] == 'while':
                p[0] = p[5]
            else:
                p[0] = p[1]
        elif self.output == YaccOutput.AST:
            if p[1] == 'if':
                if isinstance(p[5], ScopeBlock):
                    p[5] = p[5].stlist
                elif not isinstance(p[5], StmtList):
                    p[5] = StmtList([p[5]])

                if isinstance(p[7], ScopeBlock):
                    p[7] = p[7].stlist
                elif not isinstance(p[7], StmtList):
                    p[7] = StmtList([p[7]])

                p[0] = IfStatement(p[1], p[3], p[5], p[7])
            elif p[1] == 'while':
                if isinstance(p[5], ScopeBlock):
                    p[5] = p[5].stlist
                elif not isinstance(p[5], StmtList):
                    p[5] = StmtList([p[5]])
                
                p[0] = WhileStatement(p[1], p[3], p[5])
            else:
                p[0] = p[1]

    def p_unmatched_stmt(self, p):
        '''
            unmatched_stmt : IF LPAREN condition RPAREN stmt
                            | WHILE LPAREN condition RPAREN unmatched_stmt
                            | IF LPAREN condition RPAREN matched_stmt ELSE unmatched_stmt
        '''
        if self.output == YaccOutput.STATS:
            if p[1] == 'if':
                try:
                    p[0] = p[5] + p[7]
                except:
                    p[0] = p[5]
            elif p[1] == 'while':
                p[0] = p[5]
        elif self.output == YaccOutput.AST:
            if p[1] == 'if':
                try:
                    if not isinstance(p[7], StmtList):
                        p[7] = StmtList([p[7]])
                    if isinstance(p[5], ScopeBlock):
                        p[5] = p[5].stlist
                    elif not isinstance(p[5], StmtList):
                        p[5] = StmtList([p[5]])
                    p[0] = IfStatement(p[1], p[3], p[5], p[7])
                except Exception:
                    if isinstance(p[5], ScopeBlock):
                        p[5] = p[5].stlist
                    elif not isinstance(p[5], StmtList):
                        p[5] = StmtList([p[5]])
                    p[0] = IfStatement(p[1], p[3], p[5])
            elif p[1] == 'while':
                if not isinstance(p[5], StmtList):
                    p[5] = StmtList([p[5]])
                p[0] = WhileStatement(p[1], p[3], p[5])
            

    def p_condition(self, p):
        '''
            condition : condition LOGICAL_OR condition
                        | condition LOGICAL_AND condition 
        '''
        if self.output == YaccOutput.AST:
            p[0] = BinOp(Operator.arith_sym_to_op(p[2]), p[1], p[3])

    def p_condition_not(self, p):
        '''
            condition : LOGICAL_NOT condition
        '''
        if self.output == YaccOutput.AST:
            p[0] = UnaryOp(Operator.arith_sym_to_op(p[1]), p[2])

    def p_condition_paren(self, p):
        '''
            condition : LPAREN condition RPAREN
        '''
        if self.output == YaccOutput.AST:
            p[0] = p[2]

    def p_condition_end(self, p):
        '''
            condition : expr DOUBLE_EQUAL expr
                        | expr NOT_EQUAL expr
                        | expr LESS_THAN expr
                        | expr GREATER_THAN expr
                        | expr LESS_EQUAL expr
                        | expr GREATER_EQUAL expr
        '''
        if self.output == YaccOutput.AST:
            p[0] = BinOp(Operator.arith_sym_to_op(p[2]), p[1], p[3])

    def p_expr(self, p):
        '''
            expr : notNumExpr
                | onlyNumExpr
        '''
        if self.output == YaccOutput.AST:
            p[0] = p[1]

    def p_block(self, p):
        '''
            block : LCURLY stlist RCURLY
        '''
        if self.output == YaccOutput.STATS:
            p[0] = p[2]
        elif self.output == YaccOutput.AST:
            p[0] = ScopeBlock(p[2])

    def p_other(self, p):
        '''
            other : declaration SEMICOLON
                    | block
                    | assignment SEMICOLON
                    | proc_call SEMICOLON
                    | SEMICOLON
        '''
        if p[1] != ';':
            if self.output == YaccOutput.STATS:
                p[0] = p[1]
            elif self.output == YaccOutput.AST:
                p[0] = p[1]
        else:
            if self.output == YaccOutput.AST:
                p[0] = StmtList()

#######################################################################

    def p_proc_call(self, p):
        '''
            proc_call : ID LPAREN exprlist RPAREN
        '''
        if self.output == YaccOutput.AST:
            p[0] = FuncCall(p[1], p[3])

    def p_exprlist(self, p):
        '''
            exprlist : expr exprlist_helper
                    | epsilon
        '''
        if self.output == YaccOutput.AST:
            try:
                p[0] = [p[1]] + p[2]
            except:
                p[0] = []

    def p_exprlist_helper(self, p):
        '''
            exprlist_helper : COMMA expr exprlist_helper
                            | epsilon
        '''
        if self.output == YaccOutput.AST:
            try:
                p[0] = [p[2]] + p[3]
            except:
                p[0] = []

#######################################################################

    def p_declaration(self, p):
        '''
            declaration : type var varlist
        '''
        if self.output == YaccOutput.STATS:
            p[0] = p[2] + p[3]
        elif self.output == YaccOutput.AST:
            p[0] = [p[2]] + p[3]
            for var in p[0]:
                var.datatype = p[1](var.datatype)
            p[0] = Declaration(p[0])

    def p_dec_varlist(self, p):
        '''
            varlist : COMMA var varlist
                    | epsilon
        '''
        if self.output == YaccOutput.STATS:
            try:
                p[0] = p[2] + p[3]
            except:
                p[0] = Stats((0, 0, 0))
        elif self.output == YaccOutput.AST:
            try: 
                p[0] = [p[2]] + p[3]
            except:
                p[0] = []

    def p_type(self, p):
        '''
            type : INT
                | FLOAT
        '''
        if self.output == YaccOutput.AST:
            if p[1] == 'int':
                p[0] = IntType
            elif p[1] == 'float':
                p[0] = FloatType

    def p_var(self, p):
        '''
            var : ID
                | STR var %prec DEREF
        '''
        if self.output == YaccOutput.STATS:
            if p[1] == '*':
                p[0] = Stats((0, 1, 0))
            else:
                p[0] = Stats((1, 0, 0))
        elif self.output == YaccOutput.AST:
            if p[1] == '*':
                p[0] = p[2] + 1
            else:
                p[0] = Symbol(p[1])

#######################################################################

    def p_assignment(self, p):
        '''
            assignment :  ID EQUALS notNumExpr
                        | STR ptr ID EQUALS notNumExpr %prec DEREF
                        | STR ptr ID EQUALS onlyNumExpr %prec DEREF
        '''
        if self.output == YaccOutput.STATS:
            p[0] = Stats((0, 0, 1))
        elif self.output == YaccOutput.AST:
            if len(p) == 6:
                temp = Var(p[3])
                if p[2] != '':
                    for i in range(len(p[2]) - 1, -1, -1):
                        if p[2][i] == '&':
                            temp = UnaryOp(Operator.ref, temp)
                        else:
                            temp = UnaryOp(Operator.ptr, temp)

                temp = UnaryOp(Operator.ptr, temp)

                p[0] = BinOp(Operator.equal, temp, p[5])
            elif len(p) == 4:
                p[0] = BinOp(Operator.equal, Var(p[1]), p[3])

    def p_notNumExpr(self, p):
        '''
            notNumExpr : notNumExpr PLUS onlyNumExpr
                        | notNumExpr MINUS onlyNumExpr
                        | notNumExpr STR onlyNumExpr
                        | notNumExpr DIVIDE onlyNumExpr

                        | onlyNumExpr PLUS notNumExpr
                        | onlyNumExpr MINUS notNumExpr
                        | onlyNumExpr STR notNumExpr
                        | onlyNumExpr DIVIDE notNumExpr
                        
                        | notNumExpr PLUS notNumExpr
                        | notNumExpr MINUS notNumExpr
                        | notNumExpr STR notNumExpr
                        | notNumExpr DIVIDE notNumExpr             
        '''
        if self.output == YaccOutput.AST:
            p[0] = BinOp(Operator.arith_sym_to_op(p[2]), p[1], p[3])

    def p_notNumExpr_uminus(self, p):
        '''
            notNumExpr : MINUS notNumExpr %prec UMINUS
        '''
        if self.output == YaccOutput.AST:
            p[0] = UnaryOp(Operator.uminus, p[2])

    def p_notNumExpr_group(self, p):
        '''
            notNumExpr : LPAREN notNumExpr RPAREN
        '''
        if self.output == YaccOutput.AST:
            p[0] = p[2]

    def p_notNumExpr_leaf(self, p):
        '''
            notNumExpr : ptr ID
                        | ptr proc_call
        '''
        if self.output == YaccOutput.AST:
            if isinstance(p[2], str):
                temp = Var(p[2])
            elif isinstance(p[2], FuncCall):
                temp = p[2]
            if p[1] != '':
                for i in range(len(p[1]) - 1, -1, -1):
                    if p[1][i] == '&':
                        temp = UnaryOp(Operator.ref, temp)
                    else:
                        temp = UnaryOp(Operator.ptr, temp)
            p[0] = temp
            

    def p_onlyNumExpr(self, p):
        '''
            onlyNumExpr : onlyNumExpr PLUS onlyNumExpr
                | onlyNumExpr MINUS onlyNumExpr
                | onlyNumExpr STR onlyNumExpr
                | onlyNumExpr DIVIDE onlyNumExpr
        '''
        if self.output == YaccOutput.AST:
            p[0] = BinOp(Operator.arith_sym_to_op(p[2]), p[1], p[3])

    def p_onlyNumExpr_uminus(self, p):
        '''
            onlyNumExpr : MINUS onlyNumExpr %prec UMINUS
        '''
        if self.output == YaccOutput.AST:
            p[0] = UnaryOp(Operator.uminus, p[2])


    def p_onlyNumExpr_group(self, p):
        '''
            onlyNumExpr : LPAREN onlyNumExpr RPAREN
        '''
        if self.output == YaccOutput.AST:
            p[0] = p[2]

    def p_onlyNumExpr_leaf(self, p):
        '''
            onlyNumExpr : NUM
        '''
        if self.output == YaccOutput.AST:
            p[0] = Num(p[1])

    def p_ptr(self, p):
        '''
            ptr : STR ptr %prec DEREF
                | REF ptr
                | epsilon
        '''
        if self.output == YaccOutput.AST:
            try:
                p[0] = p[1] + p[2]
            except:
                p[0] = ''

    def p_error(self, p):
        if p:
            eprint("syntax error at ({1}:{2}): {0}".format(p.value, p.lineno, p.lexpos))
        else:
            eprint("syntax error at EOF")

#######################################################################
########################## Grammar Ends Here ##########################
#######################################################################

    def build(self, lexer, **kwargs):
        self.yacc = yacc.yacc(module=self, write_tables=self.write_tables, debug=True, **kwargs)
        self.lexer = lexer.lexer

    def parse(self, data):
        return self.yacc.parse(data, lexer=self.lexer)
