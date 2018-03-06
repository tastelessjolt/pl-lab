from st import *

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

    def traverse_block(self, blockblock, nextblock):
        self.traverse_ast(blockblock.stlist, nextblock)
        blockblock.goto = nextblock

    def traverse_ast(self, stlist, nextblock=BasicBlock()):
        block_list = []
        localblocks = []

        j = 0
        while(j < len(stlist)):
            # IfBlock
            if isinstance(stlist[j], IfStatement):
                localblocks.append(IfBlock([stlist[j]], self.numblocks))
                self.numblocks += 1
                block_list = []
                j += 1
            # While Block
            elif isinstance(stlist[j], WhileStatement):
                localblocks.append(WhileBlock([stlist[j]], self.numblocks))
                self.numblocks += 1
                block_list = []
                j += 1
            # Basic Block
            elif isinstance(stlist[j], ScopeBlock):
                localblocks.append(BasicBlock(stlist[j].stlist, self.numblocks))
                self.numblocks += 1
                block_list = []
                j += 1
            else:
                while(not (isinstance(stlist[j], IfStatement) or \
                        isinstance(stlist[j], WhileStatement) or \
                        isinstance(stlist[j], ScopeBlock) )):
                    block_list.append(stlist[j])
                    j += 1
                localblocks.append(BasicBlock(block_list, self.numblocks))
                self.numblocks += 1
                block_list = []

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

