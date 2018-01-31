from utils import *
from lex import *
from yacc import *
import sys
import argparse

VERSION = '0.1.0'

def process(data):
    lex.lex()
    yacc.yacc()
    yacc.parse(data)

def buildArgParser():
    parser = argparse.ArgumentParser(description='APL Compiler ver ' + VERSION)
    parser.add_argument('input_file', type=str,
                        help='program to compile')
    parser.add_argument('-l', '--lex', help='generate lex output', action='store_true')
    parser.add_argument('-y', '--yacc', help='generate yacc output', action='store_true')
    return parser

if __name__ == '__main__':

    parser = buildArgParser()
    args = parser.parse_args()

    lexer = APLLexer()
    lexer.build()

    parser = APLYacc()
    parser.build(lexer)

    filename = args.input_file
    data = open(filename, 'r').read()

    if args.lex:
        lexer.test_t(data)

    if args.yacc or not (args.lex or args.yacc):
        stats = parser.parse(data)
        if stats is not None:
            print(stats.t)
        else: 
            eprint("Exited due to above errors")
