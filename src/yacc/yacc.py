import ply.yacc as yacc
from lex import *
import operator

'''
Parsing with yacc
'''

# # TODO
# precedence = (

# )


class Stats:

    def __init__(self, t):
        self.t = t

    def __add__(self, other):
        return Stats(tuple(map(operator.add, self.t, other.t)))


class APLYacc(object):
    reserved = APLLexer.reserved
    tokens = APLLexer.tokens

    STAGE_ONE_STRUCT = (
        0,  # no of variables
        0,  # no of pointers
        0  # no of assignments
    )

    def p_program_main(self, p):
        '''
                program : VOID MAIN LPAREN RPAREN LCURLY body RCURLY
        '''
        p[0] = p[6]

    def p_function_statements(self, p):
        '''
                body : statement SEMICOLON 
                        | statement SEMICOLON body
        '''
        try:
            p[0] = p[1] + p[3]
        except Exception:
            p[0] = p[1]

    def p_statements(self, p):
        ''' 
                statement : type idlist 
        '''
        # | ID EQUALS expression
        # | PTR ID EQUALS expression
        try:
            if p[2] == '=':
                p[0] = p[3]
                p[0][2] = p[0][2] + 1
            elif p[3] == '=':
                p[0] = p[3]
                p[0][2] = p[0][2] + 1
            else:
                p[0] = p[1]
        except Exception:
            p[0] = p[2]

    def p_idlist(self, p):
        '''
                idlist : id COMMA idlist 
                                | id 
        '''

        try:
            p[0] = p[1] + p[3]
        except Exception:
            p[0] = p[1]

    def p_id(self, p):
        '''
                id : ID 
                        | PTR id
        '''
        if len(p) == 1:
            p[0] = Stats((1, 0, 0))
        else:
            p[0] = Stats((0, 1, 0))

    def p_type(self, p):
        '''
                type : INT
        '''
        p[0] = p[1]

    # def p_expression(self, p):
    # 	'''
    # 		expression :
    # 	'''

    def p_error(self, p):
        if p:
            print("syntax error at {0}".format(p.value))
        else:
            print("syntax error at EOF")

    def build(self, **kwargs):
        self.yacc = yacc.yacc(module=self, **kwargs)

    def parse(self, data, lexer):
        return self.yacc.parse(data, lexer=lexer.lexer)
