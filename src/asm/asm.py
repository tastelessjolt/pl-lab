import utils

all_instructions = []

class ASM:
    pass

class SPIM(ASM):
    def __init__(self, cfg):
        self.cfg = cfg
        self.instructions = all_instructions

class Instruction:
    def __init__(self, opcode, operands):
        self.opcode = opcode
        self.operands = operands

    def __repr__(self):
        print(self.opcode, self.operands)

class RInstruction(Instruction):
    def __init__(self, opcode, operands):
        utils._super(self).__init__(opcode, operands)

class IInstruction(Instruction):
    def __init__(self, opcode, operands):
        utils._super(self).__init__(opcode, operands)

class JInstruction(Instruction):
    def __init__(self, opcode, operands):
        utils._super(self).__init__(opcode, operands)

