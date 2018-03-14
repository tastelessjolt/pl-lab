import os
import sys
from st import *
from lex import APLLexer
from yacc import APLYacc, YaccOutput

class TestAST(object):
    tests_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../testcases/')
    tests_out = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outputs/')
    ast_tests_dir = os.path.join(tests_dir, 'st')

    def test_common(self, capsys):
        for file in os.listdir(TestAST.tests_dir):
            filepath = os.path.join(TestAST.tests_dir, file)
            if os.path.isfile(filepath) and file.endswith(".c"):
                lexer = APLLexer()
                lexer.build()

                parser = APLYacc(output = YaccOutput.AST)
                parser.build(lexer)

                f = open(filepath)
                ast = parser.parse(f.read())

                ast_str = ''
                if ast:
                    ast_str += 'Successfully Parsed\n'
                    ast_str += str(ast)

                output = open(os.path.join(TestAST.tests_out, file)).read()
                errout = capsys.readouterr().err
                print(file)
                assert output.strip() == (errout + ast_str).strip()

    def test_ast_only(self, capsys):
        for file in os.listdir(TestAST.ast_tests_dir):
            filepath = os.path.join(TestAST.ast_tests_dir, file)
            if os.path.isfile(filepath) and file.endswith(".c"):
                lexer = APLLexer()
                lexer.build()

                parser = APLYacc(output = YaccOutput.AST)
                parser.build(lexer)

                f = open(filepath)
                ast = parser.parse(f.read())

                ast_str = ''
                if ast:
                    ast_str += 'Successfully Parsed\n'
                    ast_str += str(ast)
                    
                output = open(os.path.join(TestAST.tests_out, file)).read()
                errout = capsys.readouterr().err
                print(file)
                assert output.strip() == (errout + ast_str).strip()
