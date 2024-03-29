import sys
import os
from lex import APLLexer

class TestLex(object):
    tests_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../testcases/')
    tests_out = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outputs/')
    lex_tests_dir = os.path.join(tests_dir, 'lex')

    def execute_test(self, file, filepath, capsys):
        lexer = APLLexer()
        lexer.build()
        f = open(filepath)
        l = lexer.scan(f.read())

        output = open(os.path.join(TestLex.tests_out, file)).read()
        assert output.strip() == (capsys.readouterr().err + l.__str__().strip())

    def test_common(self, capsys):
        for file in os.listdir(TestLex.tests_dir):
            filepath = os.path.join(TestLex.tests_dir, file)
            if os.path.isfile(filepath) and file.endswith(".c"):
                self.execute_test(file, filepath, capsys)

    def test_lex_only(self, capsys):
        for file in os.listdir(TestLex.lex_tests_dir):
            filepath = os.path.join(TestLex.lex_tests_dir, file)
            if os.path.isfile(filepath) and file.endswith(".c"):
                self.execute_test(file, filepath, capsys)
