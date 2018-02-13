import os
import sys
from st import *

class TestAST(object):
    tests_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../testcases/')
    tests_out = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outputs/')
    ast_tests_dir = os.path.join(tests_dir, 'ast')

    # def test_common(self, capsys):
    #     lexer = APLLexer()
    #     lexer.build()

    #     for file in os.listdir(TestLex.tests_dir):
    #         filepath = os.path.join(TestLex.tests_dir, file)
    #         if os.path.isfile(filepath):
    #             f = open(filepath)
    #             l = lexer.scan(f.read())

    #             output = open(os.path.join(TestLex.tests_out, file)).read()
    #             assert output.strip() == (capsys.readouterr().err + l.__str__().strip())

    # def test_ast_only(self, capsys):
    #     lexer = APLLexer()
    #     lexer.build()

    #     for file in os.listdir(TestLex.ast_tests_dir):
    #         filepath = os.path.join(TestLex.ast_tests_dir, file)
    #         if os.path.isfile(filepath):
    #             f = open(filepath)
    #             l = lexer.scan(f.read())
    #             output = open(os.path.join(TestLex.tests_out, file)).read()
    #             assert output.strip() == (capsys.readouterr().err + l.__str__().strip())