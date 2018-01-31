import sys
import os
from lex import APLLexer
from yacc import APLYacc

class TestYacc(object):
    tests_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../testcases/')
    tests_out = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outputs/')
    lex_tests_dir = os.path.join(tests_dir, 'yacc')

    def test_common(self):
        lexer = APLLexer()
        lexer.build()

        parser = APLYacc()
        parser.build(lexer)

        for file in os.listdir(TestYacc.tests_dir):
            filepath = os.path.join(TestYacc.tests_dir, file)
            if os.path.isfile(filepath):
                f = open(filepath)
                l = parser.parse(f.read())

                output = open(os.path.join(TestYacc.tests_out, file)).read()
                assert output.strip() == l.t.__str__().strip()

    def test_yacc_only(self, capsys):
        lexer = APLLexer()
        lexer.build()

        for file in os.listdir(TestYacc.lex_tests_dir):
            parser = APLYacc()
            parser.build(lexer)
            filepath = os.path.join(TestYacc.lex_tests_dir, file)
            if os.path.isfile(filepath):
                f = open(filepath)
                l = parser.parse(f.read())
                output = open(os.path.join(TestYacc.tests_out, file)).read()
                if l is not None:
                    assert output.strip() == (capsys.readouterr().err + l.t.__str__()).strip()
                else:
                    assert output.strip() == capsys.readouterr().err.strip()