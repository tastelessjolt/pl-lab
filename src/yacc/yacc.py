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
        except:
            p[0] = p[1]

    def p_statements(self, p):
        '''
                statement : type idlist
                            | assignment
        '''
        # | ID EQUALS expression
        # | PTR ID EQUALS expression
        try:
            p[0] = p[2]
        except:
            p[0] = p[1]

    def p_assignment(self, p):
        '''
            assignment : ID expression1 REF ID COMMA assignment
                        | ptr ID expression2 ref_val COMMA assignment
                        | ID expression1 REF ID
                        | ptr ID expression2 ref_val
        '''
        try:
            p[0] = p[6] + Stats((0, 0, 1))
        except:
            p[0] = Stats((0, 0, 1))

    def p_expression1(self, p):
        '''
            expression1 : EQUALS
                        | EQUALS ID expression1
        '''
        try:
            p[0] = p[3] + Stats((0, 0, 1))
        except:
            p[0] = Stats((0, 0, 1))

    def p_expression2(self, p):
        '''
            expression2 : EQUALS
                        | EQUALS ptr ID expression2
        '''
        try:
            p[0] = p[4] + Stats((0, 0, 1))
        except:
            p[0] = Stats((0, 0, 1))

    def p_ref_val(self, p):
        '''
            ref_val : ptr ID
                    | NUM
        '''
        pass

    def p_idlist(self, p):
        '''
            idlist : id COMMA idlist
                    | id
        '''
        try:
            p[0] = p[1] + p[3]
        except:
            p[0] = p[1]

    def p_id(self, p):
        '''
            id : ID
                | ptr ID
        '''
        if len(p) == 2:
            p[0] = Stats((1, 0, 0))
        else:
            p[0] = Stats((0, 1, 0))

    def p_ptr(self, p):
        '''
                ptr : PTR ptr
                    | PTR
        '''
        pass

    def p_type(self, p):
        '''
                type : INT
        '''
        pass

    def p_error(self, p):
        if p:
            print("syntax error at {0}".format(p.value))
        else:
            print("syntax error at EOF")

    def build(self, **kwargs):
        self.yacc = yacc.yacc(module=self, debug = True, **kwargs)

    def parse(self, data, lexer):
        return self.yacc.parse(data, lexer=lexer.lexer)
