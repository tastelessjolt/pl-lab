import sys
import os
from lex import APLLexer
from yacc import APLYacc
from yacc import YaccOutput

class TestYacc(object):
    tests_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../testcases/')
    tests_out = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outputs/')
    lex_tests_dir = os.path.join(tests_dir, 'yacc')

    def test_common(self, capsys):

        for file in os.listdir(TestYacc.tests_dir):
            filepath = os.path.join(TestYacc.tests_dir, file)
            if os.path.isfile(filepath) and file.endswith(".c"):
                lexer = APLLexer()
                lexer.build()

                parser = APLYacc(output=YaccOutput.STATS)
                parser.build(lexer)

                f = open(filepath)
                l = parser.parse(f.read())

                output = open(os.path.join(TestYacc.tests_out, file)).read()
                if l is not None:
                    assert output.strip() == (capsys.readouterr().err + l.t.__str__()).strip()
                else:
                    assert output.strip() == capsys.readouterr().err.strip()

    def test_yacc_only(self, capsys):

        for file in os.listdir(TestYacc.lex_tests_dir):
            filepath = os.path.join(TestYacc.lex_tests_dir, file)
            if os.path.isfile(filepath) and file.endswith(".c"):
                lexer = APLLexer()
                lexer.build()
                parser = APLYacc(output=YaccOutput.STATS)
                parser.build(lexer)
                f = open(filepath)
                l = parser.parse(f.read())
                output = open(os.path.join(TestYacc.tests_out, file)).read()
                if l is not None:
                    assert output.strip() == (capsys.readouterr().err + l.t.__str__()).strip()
                else:
                    assert output.strip() == capsys.readouterr().err.strip()