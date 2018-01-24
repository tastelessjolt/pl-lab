import ply.lex as lex

reserved = {'int': 'INT',
            'main': 'MAIN',
            'void': 'VOID'}

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

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)