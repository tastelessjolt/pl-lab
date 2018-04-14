from st import *

class BasicBlock(object):
    def __init__(self, astlist=StmtList(), blocknum=-1, goto=-1, end=False, func=''):
        self.astlist = astlist
        self.blocknum = blocknum
        self.goto = goto
        self.end = end
        self.expandedAst = StmtList()
        self.func = func

    def __str__(self):
        if self.end:
            return '<bb %d>\n%s\n' % (self.blocknum, 'End')
        else:
            s = self.func + '<bb %d>\n%s\n' % (self.blocknum, self.expandedAst.src())
            # Return Statement
            if self.goto != -1:
                s += "goto <bb %d>\n" % self.goto
            return s

    def expandTree(self, cfg):
        self.expandedAst = StmtList()
        for stmt in self.astlist:
            stmt.expand(cfg, self)
    
    def get_asm(self, parser, asm):
        return "\n".join([ast.get_asm(parser, asm) for ast in self.expandedAst])

    def assign_goto(self, goto):
        self.goto = goto

class IfBlock(object):
    def __init__(self, ifstmt, blocknum=-1, gotoif=-1, gotoelse=-1, func=''):
        self.ifstmt = ifstmt
        self.blocknum = blocknum
        self.gotoif = gotoif
        self.gotoelse = gotoelse
        self.expandedAst = StmtList()
        self.func = func

    def __str__(self):
        s = self.func + '<bb %d>\n%s\n' % (self.blocknum, self.expandedAst.src())
        s += 'if(%s) goto ' % (repr(self.condition))
        if self.gotoif != -1:
            s += "<bb %d>" % self.gotoif
        else:
            s += 'end'

        s += '\nelse goto '
        if self.gotoelse != -1:
            s += "<bb %d>" % self.gotoelse
        else:
            s += 'end'

        return s + '\n'

    def expandTree(self, cfg):
        self.expandedAst = StmtList()
        self.condition = self.ifstmt.condition.expand(cfg, self)

    def assign_goto(self, goto):
        if self.gotoif == -1:
            self.gotoif = goto
        
        if self.gotoelse == -1:
            self.gotoelse = goto

class WhileBlock(object):
    def __init__(self, whilestmt, blocknum=-1, gotoif=-1, gotoelse=-1, func=''):
        self.whilestmt = whilestmt
        self.blocknum = blocknum
        self.gotoif = gotoif
        self.gotoelse = gotoelse
        self.expandedAst = StmtList()
        self.func = func

    def __str__(self):
        s = self.func + '<bb %d>\n%s\n' % (self.blocknum, self.expandedAst.src())
        s += 'if(%s) goto ' % (repr(self.condition))
        if self.gotoif != -1:
            s += "<bb %d>" % self.gotoif
        else:
            s += 'end'

        s += '\nelse goto '
        if self.gotoelse != -1:
            s += "<bb %d>" % self.gotoelse
        else:
            s += 'end'

        return s + '\n'

    def expandTree(self, cfg):
        self.expandedAst = StmtList()
        self.condition = self.whilestmt.condition.expand(cfg, self)

    def assign_goto(self, goto):
        if self.gotoif == -1:
            self.gotoif = goto
        self.gotoelse = goto

class CFG(object):
    def __init__(self, programAST):
        self.ast = programAST
        self.blocks = []
        self.numblocks = 0
        self.numtemps = 0
        self.func_to_blocknum = {}

        global_list = self.ast.global_list
        for func in global_list:
            if isinstance(func, Func): # and func.fname != 'main':
                old_numblocks = self.numblocks
                unassigned = self.dfs_traverse_ast(func.stlist)
                ## TODO: WHY??
                if old_numblocks != self.numblocks:
                    self.func_to_blocknum[func.fname] = old_numblocks
                    self.blocks[old_numblocks].func += 'function %s%s\n' % (func.fname, symbol_list_as_dict(func.params))
                for blk in unassigned:
                    blk.assign_goto(self.numblocks)
                
                if len(unassigned) > 0:
                    self.blocks.append(BasicBlock(astlist=StmtList([ Return(Nothing(), type=VoidType()) ]), goto=-1, blocknum=self.numblocks))
                    self.numblocks += 1

        self.generate_expr_evals()
    
    def generate_expr_evals(self):
        for block in self.blocks:
            block.expandTree(self)

    def dfs_traverse_if(self, ifstmt):
        ifblk = IfBlock(ifstmt, self.numblocks, gotoif=self.numblocks+1)
        self.numblocks += 1
        self.blocks.append(ifblk)
        ifnotassigned = False

        unassigned = self.dfs_traverse_ast(ifstmt.stlist1)
        if ifblk.gotoif == self.numblocks:
            ifblk.gotoif = -1
            ifnotassigned = True

        ifblk.gotoelse = self.numblocks
        
        unassigned += self.dfs_traverse_ast(ifstmt.stlist2)
        if ifblk.gotoelse == self.numblocks:
            ifblk.gotoelse = -1
            ifnotassigned = True

        if ifnotassigned:
            unassigned.append(ifblk)

        return unassigned
        
    def dfs_traverse_while(self, whilestmt):
        whileblk = WhileBlock(whilestmt, self.numblocks, gotoif=self.numblocks+1)
        self.numblocks += 1
        self.blocks.append(whileblk)

        unassigned = self.dfs_traverse_ast(whilestmt.stlist)
        for blk in unassigned:
            blk.assign_goto(whileblk.blocknum)

        return [whileblk]

    def dfs_traverse_ast(self, stlist):
        j = 0
        unassigned = []
        while(j < len(stlist)):
            # IfBlock
            if isinstance(stlist[j], IfStatement):
                unassigned = self.dfs_traverse_if(stlist[j])
                j += 1
                if j != len(stlist):
                    for blk in unassigned:
                        blk.assign_goto(self.numblocks)
                    unassigned = []
            # While Block
            elif isinstance(stlist[j], WhileStatement):
                unassigned = self.dfs_traverse_while(stlist[j])
                j += 1
                if j != len(stlist):
                    for blk in unassigned:
                        blk.assign_goto(self.numblocks)
                    unassigned = []
            # Basic Block
            elif isinstance(stlist[j], ScopeBlock):
                unassigned = self.dfs_traverse_ast(stlist[j].stlist)
                j += 1
                if j != len(stlist):
                    for blk in unassigned:
                        blk.assign_goto(self.numblocks)
                    unassigned = []
            # Declaration
            elif isinstance(stlist[j], Declaration):
                j += 1
            # Return Statement
            elif isinstance(stlist[j], Return):
                # import pdb; pdb.set_trace()
                self.blocks.append(BasicBlock(StmtList([stlist[j]]), self.numblocks))
                self.numblocks += 1
                self.blocks[-1].goto = -1
                j += 1
            # FuncCall
            elif isinstance(stlist[j], FuncCall):
                self.blocks.append(BasicBlock(
                    StmtList([stlist[j]]), self.numblocks))
                self.numblocks += 1
                if j == len(stlist):
                    unassigned.append(self.blocks[-1])
                else:
                    self.blocks[-1].goto = self.numblocks

                j += 1
            # Other Statements
            else:
                block_list = StmtList()
                while(not (j >= len(stlist) or isinstance(stlist[j], IfStatement) or
                           isinstance(stlist[j], WhileStatement) or
                           isinstance(stlist[j], ScopeBlock) or
                           isinstance(stlist[j], Declaration) or
                           isinstance(stlist[j], Return) or
                           isinstance(stlist[j], FuncCall))):
                    block_list.append(stlist[j])
                    j += 1
                
                self.blocks.append(BasicBlock(block_list, self.numblocks))
                self.numblocks += 1
                if j == len(stlist):
                    unassigned.append(self.blocks[-1])
                else:
                    self.blocks[-1].goto = self.numblocks

        return unassigned

    def __str__(self):
        return '\n'.join ([str(block) for block in self.blocks])
