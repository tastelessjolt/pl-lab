from st import *

class BasicBlock(object):
    def __init__(self, astlist=StmtList(), blocknum=-1, goto=-1):
        self.astlist = astlist
        self.blocknum = blocknum
        self.goto = goto

    def __str__(self):
        s = '<bb %d>\n%s\ngoto ' % (self.blocknum, self.astlist.src())
        if self.goto.blocknum != -1:
            s += "<bb %d>\n" % self.goto.blocknum
        else:
            s += 'end\n'
        return s

    def expandTree(self, cfg):
        # cfg.numtemps ++
        # import pdb
        # pdb.set_trace()
        pass

class IfBlock(object):
    def __init__(self, astlist=StmtList(), blocknum=-1, gotoif=-1, gotoelse=-1):
        self.astlist = astlist
        self.blocknum = blocknum
        self.gotoif = gotoif
        self.gotoelse = gotoelse
        self.expandedAst = StmtList()

    def __str__(self):
        s = '<bb %d>\n%s\n' % (self.blocknum, self.expandedAst.src())
        s += 'if(%s) goto: ' % (repr(self.condition))
        if self.gotoif.blocknum != -1:
            s += "<bb %d>" % self.gotoif.blocknum
        else:
            s += 'end'

        s += '\nelse goto: '
        if self.gotoelse.blocknum != -1:
            s += "<bb %d>" % self.gotoelse.blocknum
        else:
            s += 'end'

        return s + '\n'

    def expandTree(self, cfg):
        self.expandedAst = StmtList()
        self.condition = self.astlist[0].condition.expand(cfg, self)

class WhileBlock(object):
    def __init__(self, astlist=StmtList(), blocknum=-1, gotoif=-1, gotoelse=-1):
        self.astlist = astlist
        self.blocknum = blocknum
        self.gotoif = gotoif
        self.gotoelse = gotoelse
        self.expandedAst = StmtList()

    def __str__(self):
        s = '<bb %d>\n%s\n' % (self.blocknum, self.expandedAst.src())
        s += 'if(%s) goto: ' % (repr(self.condition))
        if self.gotoif.blocknum != -1:
            s += "<bb %d>" % self.gotoif.blocknum
        else:
            s += 'end'

        s += '\nelse goto: '
        if self.gotoelse.blocknum != -1:
            s += "<bb %d>" % self.gotoelse.blocknum
        else:
            s += 'end'

        return s + '\n'

    def expandTree(self, cfg):
        self.expandedAst = StmtList()
        self.condition = self.astlist[0].condition.expand(cfg, self)


class CFG(object):
    def __init__(self, programAST):
        self.ast = programAST
        self.blocks = []
        self.numblocks = 0
        self.numtemps = 0

        function_list = self.ast.funclist
        main_func = [func for func in function_list if func.fname == 'main'][0]
        self.traverse_ast(main_func.stlist)

        self.blocks.sort(key=lambda block: block.blocknum)
        self.generateExprEvals()
    
    def generateExprEvals(self):
        for block in self.blocks:
            block.expandTree(self)

    def traverse_if(self, ifblock, nextblock):
        ifblock.gotoif = self.traverse_ast(ifblock.astlist[0].stlist1, nextblock)
        if ifblock.astlist[0].stlist2:
            ifblock.gotoelse = self.traverse_ast(ifblock.astlist[0].stlist2, nextblock)
        else:
            ifblock.gotoelse = nextblock

    def traverse_while(self, whileblock, nextblock):
        whileblock.gotoif = self.traverse_ast(whileblock.astlist[0].stlist, whileblock)
        whileblock.gotoelse = nextblock

    def traverse_block(self, blockblock, nextblock):
        self.traverse_ast(blockblock.stlist, nextblock)
        blockblock.goto = nextblock

    def traverse_ast(self, stlist, nextblock=BasicBlock()):
        localblocks = []
        block_list = StmtList()

        j = 0
        while(j < len(stlist)):
            # IfBlock
            if isinstance(stlist[j], IfStatement):
                localblocks.append(IfBlock([stlist[j]], self.numblocks))
                self.numblocks += 1
                block_list = StmtList()
                j += 1
            # While Block
            elif isinstance(stlist[j], WhileStatement):
                localblocks.append(WhileBlock([stlist[j]], self.numblocks))
                self.numblocks += 1
                block_list = StmtList()
                j += 1
            # Basic Block
            elif isinstance(stlist[j], ScopeBlock):
                localblocks.append(BasicBlock(stlist[j].stlist, self.numblocks))
                self.numblocks += 1
                block_list = StmtList()
                j += 1
            elif isinstance(stlist[j], Declaration):
                j += 1
            else:
                while(not (j >= len(stlist) or isinstance(stlist[j], IfStatement) or
                        isinstance(stlist[j], WhileStatement) or \
                           isinstance(stlist[j], ScopeBlock) or \
                           isinstance(stlist[j], Declaration))):
                    block_list.append(stlist[j])
                    j += 1
                localblocks.append(BasicBlock(block_list, self.numblocks))
                self.numblocks += 1
                block_list = StmtList()

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

        ret = localblocks[0]

        localblocks.pop()
        self.blocks += localblocks

        return ret

    def __str__(self):
        return '\n'.join ([str(block) for block in self.blocks])
