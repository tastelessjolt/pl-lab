import ply.yacc as yacc
import operator
from enum import Enum
from lex import *
from ast import *
from utils import *

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
        ('left', 'DIVIDE', 'TIMES'),
        ('right', 'UMINUS'),
        ('right', 'PTR'),
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
            pass
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
            pass
            # try: 
                # p[0] = ASTStmtList(p[2], p[1])

    def p_statement(self, p):
        '''
            statement : declaration SEMICOLON
                        | assignments SEMICOLON
        '''
        if self.output == YaccOutput.STATS:
            p[0] = p[1]
        elif self.output == YaccOutput.AST:
            pass

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
            pass

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
            pass

    def p_assignment(self, p):
        '''
            assignment :  ID EQUALS ptr ID
                        | PTR ptr ID EQUALS expr
        '''
        if self.output == YaccOutput.STATS:
            p[0] = Stats((0, 0, 1))
        elif self.output == YaccOutput.AST:
            pass

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
            pass

    def p_expr_uminus(self, p):
        ''' 
            expr : MINUS expr %prec UMINUS
        '''
        pass

    def p_expr_group(self, p):
        '''
            expr : LPAREN expr RPAREN
        '''
        pass

    def p_expr_leaf(self, p):
        '''
            expr : ptr ID 
                | NUM
        '''
        pass
        # try:
        #     p[0] = p[2]
        # except:
        #     p[0] = p[1]

    def p_ptr(self, p):
        '''
            ptr : PTR ptr
                | REF ptr
                | epsilon
        '''
        if self.output == YaccOutput.STATS:
            pass
        elif self.output == YaccOutput.AST:
            pass

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
