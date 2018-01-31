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
    parser.add_argument('-l', help='generate only lex output')
    parser.add_argument('-y', help='generate only yacc output')
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

    if False:
        lexer.test_t(data)
        sys.exit()

    stats = parser.parse(data)
    if stats is not None:
        print(stats.t)
    else:
        eprint("Exited due to above errors")