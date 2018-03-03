
from st import *

class CFG(object):
    class Block(object):
        def __init__(self, astlist, blocknum):
            self.astlist = astlist
            self.blocknum = blocknum

        def __str__(self):
            return NotImplementedError

    def __init__(self, programAST):
        self.ast = programAST
        self.blocks = []
        self.traverse_ast()

    def traverse_if(self, if_ast, blocknum):
        raise NotImplementedError

    def traverse_while(self, while_ast, blocknum):
        raise NotImplementedError

    def traverse_ast(self):
        block_number = 0
        function_list = self.ast.function_list
        main_func = [func for func in function_list if func.fname == 'main'][0]
        stlist = main_func.stlist
        block_list = []

        j = 0

        while(j < len(stlist)):
            while(not (isinstance(stlist[j], IfStatement) or isinstance(stlist[j], WhileStatement))):
                block_list.append(stlist[j])
                j += 1
            self.blocks.append(Block(block_list, block_number))
            block_number += 1
            block_list = []
            self.blocks.append(Block([stlist[j]], block_number))
            block_number += 1

            if isinstance(stlist[j], IfStatement):
                traverse_if(stlist[j], block_number)
            else:
                traverse_while(stlist[j], block_number)

            j += 1
