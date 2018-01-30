import ply.yacc as yacc
from lex import *
import operator

'''
Parsing with yacc
'''

# # TODO
precedence = (
    ('right', 'EQUALS'),
    ('left', 'PTR'),
)


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
    start = 'program'
    def p_program(self, p):
        '''
            program : main
        '''
        p[0] = p[1]

    def p_epsilon(self, p):
        '''
            epsilon :
        '''
        pass

    def p_main(self, p):
        '''
            main : VOID MAIN LPAREN RPAREN LCURLY body RCURLY
        '''
        p[0] = p[6]

    def p_function_body(self, p):
        '''
            body : statement stlist
        '''
        try:
            p[0] = p[1] + p[2]
        except:
            p[0] = p[1]

    def p_statements(self, p):
        '''
            stlist : statement stlist
                    | epsilon
        '''
        try:
            p[0] = p[1] + p[2] 
        except:
            p[0] = Stats((0, 0, 0))

    def p_statement(self, p):
        '''
            statement : declaration SEMICOLON
                        | assignments SEMICOLON
        '''
        p[0] = p[1]

    def p_declaration(self, p):
        '''
            declaration : type var varlist
        '''
        p[0] = p[2] + p[3]

    def p_dec_varlist(self, p):
        '''
            varlist : COMMA var varlist 
                    | epsilon
        '''
        try:
            p[0] = p[2] + p[3]
        except:
            p[0] = Stats((0, 0, 0))

    def p_type(self, p):
        '''
            type : INT
        '''
        pass

    def p_var(self, p):
        '''
            var : ID 
                | PTR var
        '''
        if p[1] == '*':
            p[0] = Stats((0, 1, 0))
        else:
            p[0] = Stats((1, 0, 0))

    def p_assignments(self, p):
        '''
            assignments : assignment assignlist
        '''
        p[0] = p[1] + p[2]

    def p_assignlist(self, p):
        '''
            assignlist : COMMA assignment assignlist 
                        | epsilon
        '''
        try: 
            p[0] = p[2] + p[3]
        except:
            p[0] = Stats((0, 0, 0))

    def p_assignment(self, p):
        '''
            assignment : ID EQUALS ID
                        | ID EQUALS REF ID
                        | PTR ID EQUALS PTR ID
                        | PTR ID EQUALS NUM
        '''
        p[0] = Stats((0, 0, 1))

    def p_error(self, p):
        if p:
            print("syntax error at {0}".format(p.value))
        else:
            print("syntax error at EOF")

    def build(self, **kwargs):
        self.yacc = yacc.yacc(module=self, debug = True, **kwargs)

    def parse(self, data, lexer):
        print(data)
        return self.yacc.parse(data, lexer=lexer.lexer)
