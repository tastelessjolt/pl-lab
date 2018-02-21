import ply.yacc as yacc
from enum import Enum
from lex import *
from st import *
from utils import *
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
    CFG = 2

class APLYacc(object):
    reserved = APLLexer.reserved
    tokens = APLLexer.tokens

    precedence = [
        ('left', 'PLUS', 'MINUS'),
        ('left', 'STR', 'DIVIDE'),
        ('right', 'UMINUS', 'DEREF', 'REF'),
        ('left', 'LESS_THAN', 'GREATER_THAN', 'LESS_EQUAL', 'GREATER_EQUAL'),
        ('left', 'DOUBLE_EQUAL'),
    ]

    def __init__(self, output=YaccOutput.AST):
        self.output = output

    start = 'program'
    def p_program(self, p):
        '''
            program : main
        '''
        if self.output == YaccOutput.STATS:
            p[0] = p[1]
        elif self.output == YaccOutput.AST:
            p[0] = p[1]

    def p_epsilon(self, p):
        '''
            epsilon :
        '''
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            pass

    def p_main(self, p):
        '''
            main : VOID MAIN LPAREN RPAREN LCURLY stlist RCURLY
        '''
        if self.output == YaccOutput.STATS:
            p[0] = p[6]
        elif self.output == YaccOutput.AST:
            p[0] = p[6]
            # p[0] = ASTFunc('main', p[6])

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
                p[0] = [p[1]] + p[2]
            except:
                p[0] = []

#######################################################################3

    def p_stmt(self, p):
        '''
            stmt : matched_stmt
                | unmatched_stmt
        '''
        p[0] = p[1]
    
    def p_matched_stmt(self, p):
        '''
            matched_stmt : IF LPAREN condition RPAREN matched_stmt ELSE matched_stmt
                        | IF LPAREN condition RPAREN block ELSE block
                        | statement
        '''
        p[0] = p[1]

    def p_unmatched_stmt(self, p):
        '''
            unmatched_stmt : IF LPAREN condition RPAREN unmatched_stmt
                            | IF LPAREN condition RPAREN matched_stmt ELSE unmatched_stmt
                            | IF LPAREN condition RPAREN block
        '''
        pass

    def p_condition(self, p):
        '''
            condition : assignment
        '''
        pass

    def p_block(self, p):
        '''
            block : LCURLY stlist RCURLY
        '''
        if self.output == YaccOutput.STATS:
            p[0] = p[2]
        elif self.output == YaccOutput.AST:
            p[0] = p[2]
        
#######################################################################3

    def p_statement(self, p):
        '''
            statement : declaration SEMICOLON
                        | assignments SEMICOLON
        '''
        if self.output == YaccOutput.STATS:
            p[0] = p[1]
        elif self.output == YaccOutput.AST:
            p[0] = p[1]

    def p_declaration(self, p):
        '''
            declaration : type var varlist
        '''
        if self.output == YaccOutput.STATS:
            p[0] = p[2] + p[3]
        elif self.output == YaccOutput.AST:
            pass

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
            pass

    def p_type(self, p):
        '''
            type : INT
        '''
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            pass

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
            pass

    def p_assignments(self, p):
        '''
            assignments : assignment assignlist
        '''
        if self.output == YaccOutput.STATS:
            p[0] = p[1] + p[2]
        elif self.output == YaccOutput.AST:
            p[0] = [p[1]] + p[2]

    def p_assignlist(self, p):
        '''
            assignlist : COMMA assignment assignlist
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
                        | onlyNumExpr PLUS notNumExpr
                        | notNumExpr MINUS onlyNumExpr
                        | onlyNumExpr MINUS notNumExpr
                        | notNumExpr STR onlyNumExpr
                        | onlyNumExpr STR notNumExpr
                        | notNumExpr DIVIDE onlyNumExpr
                        | onlyNumExpr DIVIDE notNumExpr
                        | notNumExpr PLUS notNumExpr
                        | notNumExpr MINUS notNumExpr
                        | notNumExpr STR notNumExpr
                        | notNumExpr DIVIDE notNumExpr
        '''
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            p[0] = BinOp(Operator.arith_sym_to_op(p[2]), p[1], p[3])

    def p_notNumExpr_uminus(self, p):
        '''
            notNumExpr : MINUS notNumExpr %prec UMINUS
        '''
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            p[0] = UnaryOp(Operator.uminus, p[2])

    def p_notNumExpr_group(self, p):
        '''
            notNumExpr : LPAREN notNumExpr RPAREN
        '''
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            p[0] = p[2]

    def p_notNumExpr_leaf(self, p):
        '''
            notNumExpr : ptr ID
        '''
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            temp = Var(p[2])
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
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            p[0] = BinOp(Operator.arith_sym_to_op(p[2]), p[1], p[3])

    def p_onlyNumExpr_uminus(self, p):
        '''
            onlyNumExpr : MINUS onlyNumExpr %prec UMINUS
        '''
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            p[0] = UnaryOp(Operator.uminus, p[2])


    def p_onlyNumExpr_group(self, p):
        '''
            onlyNumExpr : LPAREN onlyNumExpr RPAREN
        '''
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            p[0] = p[2]

    def p_onlyNumExpr_leaf(self, p):
        '''
            onlyNumExpr : NUM
        '''
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            p[0] = Num(p[1])

    def p_ptr(self, p):
        '''
            ptr : STR ptr %prec DEREF
                | REF ptr
                | epsilon
        '''
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            try:
                p[0] = p[1] + p[2]
            except:
                p[0] = ''

    def p_error(self, p):
        if p:
            eprint("syntax error at ({1}:{2}): {0}".format(p.value, p.lineno, p.lexpos))
        else:
            eprint("syntax error at EOF")

    def build(self, lexer, **kwargs):
        self.yacc = yacc.yacc(module=self, debug = True, **kwargs)
        self.lexer = lexer.lexer

    def parse(self, data):
        return self.yacc.parse(data, lexer=self.lexer)
