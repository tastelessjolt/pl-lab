from __future__ import print_function
from lex import *
from yacc import *
import sys
from utils import *

def process(data):
    lex.lex()
    yacc.yacc()
    yacc.parse(data)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        eprint("Usage: " + sys.argv[0] + " <filename>")
        sys.exit()

    lexer = APLLexer()
    lexer.build()

    filename = sys.argv[1]
    data = open(filename, 'r').read()

    lexer.test_t(data)