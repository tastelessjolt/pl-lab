import ply.lex as lex
from utils import *

class APLLexer(object):
    reserved = {
        'int': 'INT',
        'main': 'MAIN',
        'void': 'VOID',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE'
    }

    tokens = [
        'ID',
        'LPAREN',
        'RPAREN',
        'EQUALS',
        'STR',
        'PLUS',
        'MINUS',
        'DIVIDE',
        'SEMICOLON',
        'REF',
        'COMMA',
        'LCURLY',
        'RCURLY',
        'NUM',
        'DOUBLE_EQUAL',
        'NOT_EQUAL',
        'LESS_THAN',
        'GREATER_THAN',
        'LESS_EQUAL',
        'GREATER_EQUAL',
    ] + list(reserved.values())

    t_ignore = " \t"

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_STR = r'\*'
    t_EQUALS = r'='
    t_PLUS=r'\+'
    t_MINUS=r'\-'
    t_DIVIDE=r'\/'
    t_SEMICOLON = r';'
    t_REF = r'\&'
    t_COMMA = r'\,'
    t_LCURLY = r'\{'
    t_RCURLY = r'\}'
    t_DOUBLE_EQUAL = r'=='
    t_NOT_EQUAL = r'\!='
    t_LESS_THAN = r'<'
    t_GREATER_THAN = r'>'
    t_LESS_EQUAL = r'<='
    t_GREATER_EQUAL = r'>='

    def t_NUM(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = APLLexer.reserved.get(t.value, 'ID')
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)


    def t_error(self, t):
        eprint("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def scan(self, data):
        l = []
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            l.append((tok.value, tok.type))
        return l
