#!/usr/bin/python3

from utils import *
from lex import *
from yacc import *
import sys
import os
import argparse

VERSION = '0.3.0'

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
    parser.add_argument('-a', '--ast', help='generate ast output', action='store_true')
    return parser

if __name__ == '__main__':

    parser = buildArgParser()
    args = parser.parse_args()

    lexer = APLLexer()
    lexer.build()

    filename = args.input_file
    data = open(filename, 'r').read()

    if args.lex:
        print(lexer.scan(data))
        if not args.yacc:
            sys.exit()

    if args.yacc:
        parser = APLYacc(output = YaccOutput.STATS)
        parser.build(lexer)
        stats = parser.parse(data)
        if stats is not None:
            print(stats.t)
            if not args.ast:
                sys.exit()

    if args.ast or not (args.yacc or args.lex):
        parser = APLYacc(output = YaccOutput.AST)
        parser.build(lexer)
        ast = parser.parse(data)
        f = open ('Parser_ast_' + os.path.basename(filename), 'w')
        if ast:
            eprint("Successfully Parsed")
            for i in ast:
                if i is not None:
                    f.write(i[0].__str__() + "\n\n")
        else:
            f.write('')
        f.close()
