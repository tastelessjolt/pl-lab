from ..lex import APLLexer 
import os 

class TestClass(object):
    tests_dir = os.path.join(os.path.realpath(__file__), 'all/')
    tests_out = os.path.join(os.path.realpath(__file__), 'lex/')

    def test_files(self):
        lexer = APLLexer()
        lexer.build()

        for file in os.listdir(TestClass.tests_dir):
            f = open(os.path.join(TestClass.tests_dir, file))
            l = lexer.test(f.read())

            output = open(os.path.join(TestClass.tests_out, file)).read()
            assert output.strip() == l.__str__().strip()