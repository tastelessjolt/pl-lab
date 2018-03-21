#!/usr/bin/env python3

from utils import eprint
from lex import *
from yacc import *
from cfg import *
import sys
import os
import argparse

VERSION = '0.4.0'

def buildArgParser():
    parser = argparse.ArgumentParser(description='APL Compiler ver ' + VERSION)
    parser.add_argument('input_file', type=str,
                        help='program to compile')
    parser.add_argument('-l', '--lex', help='generate lex output', action='store_true')
    parser.add_argument('-y', '--yacc', help='generate yacc output', action='store_true')
    parser.add_argument('-a', '--ast', help='generate AST output', action='store_true')
    parser.add_argument('-c', '--cfg', help='generate CFG output', action='store_true')    
    parser.add_argument('-e', '--ecfg', help='generate Extended CFG output', action='store_true')    
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

    if args.ast:
        parser = APLYacc(output = YaccOutput.AST)
        parser.build(lexer)
        ast = parser.parse(data)
        f = open ('Parser_ast_' + os.path.basename(filename), 'w')
        if ast:
            eprint("Successfully Parsed")
            print(str(ast))
        else:
            f.write('')
        f.close()
    
    if args.cfg:
        parser = APLYacc(output = YaccOutput.AST)
        parser.build(lexer)
        ast = parser.parse(data)
        if ast:
            with open(filename + '.ast', 'w') as f:
                f.write(str(ast))

            cfg = CFG(ast)
            with open(filename + '.cfg', 'w') as f:
                f.write(str(cfg))

    if args.ecfg or not (args.yacc or args.lex or args.ast or args.cfg):
        parser = APLYacc(output=YaccOutput.AST)
        parser.build(lexer)
        ast = parser.parse(data)
        if ast:
            print (repr(ast))
            print('Procedure table :-')
            print('-----------------------------------------------------------------')
            print('Name\t\t|\tReturn Type  |  Parameter List')
            print('-----------------------------------------------------------------')
            for key, value in parser.all_symtab[0].table.items():
                if value.table_ptr and value.name != 'main':
                     print(str(value))
            print('-----------------------------------------------------------------')
            print('Variable table :-')
            print('-----------------------------------------------------------------')
            print('Name\t|\tScope\t\t|\tBase Type  |  Derived Type')
            print('-----------------------------------------------------------------')
            all_symtab_copy = parser.all_symtab[1:]
            all_symtab_copy.reverse()
            all_symtab_copy.insert(0, parser.all_symtab[0])
            for symtab in all_symtab_copy:
                for key, value in symtab.table.items():
                    if not value.table_ptr:
                        print(value.__str__('procedure ' + str(symtab.name) if symtab.name != 'global' else 'global'))
            print('-----------------------------------------------------------------')
            print('-----------------------------------------------------------------')
