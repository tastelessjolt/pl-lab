from __future__ import print_function
from lex import *
from yacc import *
import sys
import argparse

VERSION = '0.1.0'

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def process(data):
    lex.lex()
    yacc.yacc()
    yacc.parse(data)

def buildParser():
    parser = argparse.ArgumentParser(description='APL Compiler ver ' + VERSION)
    parser.add_argument('input_file', type=str,
                        help='program to compile')
    return parser

if __name__ == '__main__':

    parser = buildParser()
    args = parser.parse_args()

    lexer = APLLexer()
    lexer.build()

    filename = args.input_file
    data = open(filename, 'r').read()

    lexer.test_t(data)