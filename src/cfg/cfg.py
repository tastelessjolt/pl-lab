class CFG(object):
    class BasicBlock(object):
        def __init__(self, astlist, blocknum):
            self.astlist = astlist
            self.blocknum = blocknum

        def __str__(self):
            return NotImplementedError

    def __init__(self, programAST):
        self.ast = programAST
        self.blocks = []
        self.traverse_ast()

    def traverse_ast(self):
        raise NotImplementedError