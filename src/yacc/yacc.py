import ply.yacc as yacc
import operator
from enum import Enum
from lex import *
from ast import *
from utils import *

import pdb

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
        ('left', 'PLUS', 'MINUS'),
        ('left', 'PTR', 'DIVIDE'),
        ('right', 'UMINUS'),
        # ('right', 'PTR', 'REF'),
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
            main : VOID MAIN LPAREN RPAREN LCURLY body RCURLY
        '''
        if self.output == YaccOutput.STATS:
            p[0] = p[6]
        elif self.output == YaccOutput.AST:
            p[0] = p[6]
            # p[0] = ASTFunc('main', p[6])

    def p_function_body(self, p):
        '''
            body : stlist
        '''
        if self.output == YaccOutput.STATS:
            p[0] = p[1]
        elif self.output == YaccOutput.AST:
            p[0] = p[1]

    def p_statements(self, p):
        '''
            stlist : statement stlist
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
            # p[0] = 'DEC ' + p[1]
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
                | PTR var
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
                        | PTR ptr ID EQUALS expr
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
                        | notNumExpr PTR onlyNumExpr %prec TIMES
                        | onlyNumExpr PTR notNumExpr %prec TIMES
                        | notNumExpr DIVIDE onlyNumExpr
                        | onlyNumExpr DIVIDE notNumExpr
                        | notNumExpr PLUS notNumExpr
                        | notNumExpr MINUS notNumExpr
                        | notNumExpr PTR notNumExpr %prec TIMES
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

    ############################################################
    def p_onlyNumExpr(self, p):
        '''
            onlyNumExpr : onlyNumExpr PLUS onlyNumExpr
                | onlyNumExpr MINUS onlyNumExpr
                | onlyNumExpr PTR onlyNumExpr %prec TIMES
                | onlyNumExpr DIVIDE onlyNumExpr
        '''
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            p[0] = BinOp(Operator.arith_sym_to_op(p[2]), p[1], p[3])

    def p_expr_times(self, p):
        '''
            expr : expr PTR expr
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


    ############################################################

    def p_expr_uminus(self, p):
        '''
            expr : MINUS expr %prec UMINUS
        '''
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            p[0] = UnaryOp(Operator.uminus, p[2])

    def p_expr(self, p):
        '''
            expr : expr PLUS expr
                | expr MINUS expr
                | expr PTR expr %prec TIMES
                | expr DIVIDE expr
        '''
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            p[0] = BinOp(Operator.arith_sym_to_op(p[2]), p[1], p[3])

    def p_expr_group(self, p):
        '''
            expr : LPAREN expr RPAREN
        '''
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            p[0] = p[2]

    def p_expr_leaf(self, p):
        '''
            expr : ptr ID
                | NUM
        '''
        pdb.set_trace()
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            if len(p) == 3:
                temp = Var(p[2])
                if p[1] != '':
                    for i in range(len(p[1]) - 1, -1, -1):
                        if p[1][i] == '&':
                            temp = UnaryOp(Operator.ref, temp)
                        else:
                            temp = UnaryOp(Operator.ptr, temp)
                p[0] = temp
            elif len(p) == 2:
                p[0] = Num(p[1])

    def p_ptr(self, p):
        '''
            ptr : PTR ptr
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
