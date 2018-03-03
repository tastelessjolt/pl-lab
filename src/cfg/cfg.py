
from st import *


class BasicBlock(object):
    def __init__(self, astlist=[], blocknum=-1, goto=-1):
        self.astlist = astlist
        self.blocknum = blocknum
        self.goto = goto

    def __str__(self):
        return NotImplementedError

class IfBlock(object):
    def __init__(self, astlist=[], blocknum=-1, gotoif=-1, gotoelse=-1):
        self.astlist = astlist
        self.blocknum = blocknum
        self.gotoif = gotoif
        self.gotoelse = gotoelse

    def __str__(self):
        return NotImplementedError

class WhileBlock(object):
    def __init__(self, astlist=[], blocknum=-1, gotoif=-1, gotoelse=-1):
        self.astlist = astlist
        self.blocknum = blocknum
        self.gotoif = gotoif
        self.gotoelse = gotoelse

    def __str__(self):
        return NotImplementedError

class CFG(object):
    def __init__(self, programAST):
        self.ast = programAST
        self.blocks = []
        self.numblocks = 0

        function_list = self.ast.function_list
        main_func = [func for func in function_list if func.fname == 'main'][0]
        self.traverse_ast(main_func.stlist)


    def traverse_if(self, ifblock, nextblock):
        ifblock.gotoif = self.traverse_ast(ifblock.astlist[0].stlist1, nextblock)
        if ifblock.astlist[0].stlist2:
            ifblock.gotoelse = self.traverse_ast(ifblock.astlist[0].stlist2, nextblock)

    def traverse_while(self, whileblock, nextblock):
        whileblock.gotoif = self.traverse_ast(whileblock.astlist[0].stlist, whileblock)
        whileblock.gotoelse = nextblock

    def traverse_ast(self, stlist, nextblock=BasicBlock()):
        block_list = []

        j = 0

        localblocks = []

        while(j < len(stlist)):
            if not (isinstance(stlist[j], IfStatement) or isinstance(stlist[j], WhileStatement)):
                while(not (isinstance(stlist[j], IfStatement) or isinstance(stlist[j], WhileStatement))):
                    block_list.append(stlist[j])
                    j += 1
                # Basic Block
                localblocks.append(BasicBlock(block_list, self.numblocks))
                self.numblocks += 1
                block_list = []
            elif isinstance(stlist[j], IfStatement):
                # IfBlock
                localblocks.append(IfBlock([stlist[j]], self.numblocks))
                self.numblocks += 1
                block_list = []
                j += 1
            else:
                # While Block
                localblocks.append(WhileBlock([stlist[j]], self.numblocks))
                self.numblocks += 1
                block_list = []
                j += 1

        localblocks.append(nextblock)

        for i in range(len(localblocks) - 1):
            thisblock = localblocks[i]
            _nextblock = localblocks[i+1]
            if isinstance(thisblock, BasicBlock):
                thisblock.goto = _nextblock
            elif isinstance(thisblock, IfBlock):
                self.traverse_if(thisblock, _nextblock)
            else:
                self.traverse_while(thisblock, _nextblock)

        localblocks.pop()
        self.blocks += localblocks

        return localblocks[0]
