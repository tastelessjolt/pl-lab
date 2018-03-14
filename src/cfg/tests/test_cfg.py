import os
import sys
from st import *
from cfg import *
from lex import APLLexer
from yacc import APLYacc, YaccOutput


class TestCFG(object):
    tests_dir = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), '../../testcases/')
    tests_out = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'outputs/')
    cfg_tests_dir = os.path.join(tests_dir, 'cfg')

    def execute_test(self, file, filepath, capsys):
        lexer = APLLexer()
        lexer.build()

        parser = APLYacc(output=YaccOutput.AST)
        parser.build(lexer)

        f = open(filepath)
        ast = parser.parse(f.read())

        ast_str = ''
        if ast:
            ast_str = str(ast)

        output = open(os.path.join(
            TestCFG.tests_out, file + ".ast")).read()
        errout = capsys.readouterr().err
        assert output.strip() == (errout + ast_str).strip()

        cfg_str = ''
        if ast:
            cfg = CFG(ast)
            cfg_str = str(cfg)
        output = open(os.path.join(
            TestCFG.tests_out, file + ".cfg")).read()
        assert output.strip() == (errout + cfg_str).strip()

    def test_common(self, capsys):
        for file in os.listdir(TestCFG.tests_dir):
            filepath = os.path.join(TestCFG.tests_dir, file)
            if os.path.isfile(filepath) and file.endswith(".c"):
                self.execute_test(file, filepath, capsys)


    def test_cfg_only(self, capsys):
        for file in os.listdir(TestCFG.cfg_tests_dir):
            filepath = os.path.join(TestCFG.cfg_tests_dir, file)
            if os.path.isfile(filepath) and file.endswith(".c"):
                self.execute_test(file, filepath, capsys)
