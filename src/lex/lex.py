import ply.lex as lex
from utils import *

class APLLexer(object):
    reserved = {
        'int': 'INT',
        'main': 'MAIN',
        'void': 'VOID'
    }

    tokens = [
        'ID',
        'LPAREN',
        'RPAREN',
        'EQUALS',
        'PTR',
        'SEMICOLON',
        'REF',
        'COMMA',
        'LCURLY',
        'RCURLY',
        'NUM'
    ] + list(reserved.values())

    t_ignore = " \t\n"

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_PTR = r'\*'
    t_EQUALS = r'='
    t_SEMICOLON = r';'
    t_REF = r'\&'
    t_COMMA = r'\,'
    t_LCURLY = r'\{'
    t_RCURLY = r'\}'
    t_NUM = r'\d+'

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = APLLexer.reserved.get(t.value, 'ID')
        return t

    def t_error(self, t):
        eprint("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        l = []
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            l.append((tok.value, tok.type))
        return l

    # Test it output
    def test_t(self, data):
        l = []
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            l.append((tok.value, tok.type))
        print(l)