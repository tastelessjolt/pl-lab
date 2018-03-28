import sys
import os

from lex import APLLexer
from yacc import APLYacc, YaccOutput
from cfg import CFG
from utils import symtab_from_ast

class TestSymtab(object):
    tests_dir = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), '../../testcases/')
    tests_out = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'outputs/')
    symtab_tests_dir = os.path.join(tests_dir, 'symtab')

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
            TestSymtab.tests_out, file + ".ast")).read()
        errout = capsys.readouterr().err
        assert output.strip() == (errout + ast_str).strip()

        cfg_str = ''
        if ast:
            cfg = CFG(ast)
            cfg_str = str(cfg)
        output = open(os.path.join(
            TestSymtab.tests_out, file + ".cfg")).read()
        assert output.strip() == (errout + cfg_str).strip()

        symtab_str = ''
        if ast:
            symtab_str = symtab_from_ast(parser, ast)
        output = open(os.path.join(
            TestSymtab.tests_out, file + ".sym")).read()
        assert output.strip() == (errout + symtab_str).strip()

    def test_common(self, capsys):
        for file in os.listdir(TestSymtab.tests_dir):
            filepath = os.path.join(TestSymtab.tests_dir, file)
            if os.path.isfile(filepath) and file.endswith(".c"):
                self.execute_test(file, filepath, capsys)

    def test_symtab_only(self, capsys):
        for file in os.listdir(TestSymtab.symtab_tests_dir):
            filepath = os.path.join(TestSymtab.symtab_tests_dir, file)
            if os.path.isfile(filepath) and file.endswith(".c"):
                self.execute_test(file, filepath, capsys)
