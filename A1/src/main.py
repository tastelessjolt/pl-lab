from __future__ import print_function
from lex import *
from yacc import *
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def process(data):
    lex.lex()
    yacc.yacc()
    yacc.parse(data)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        eprint("Usage: " + argv[0] + " <filename>")
        sys.exit()

    l = lex.lex(debug=1)
    lex.runmain()
    # filename = sys.argv[1]
    # data = open(filename, 'r').read()
    # process(data)