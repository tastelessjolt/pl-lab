import utils

all_instructions = []

class ASM:
    pass

class SPIM(ASM):
    def __init__(self, parser, cfg):
        self.cfg = cfg
        self.parser = parser
        self.instructions = all_instructions

    def get_data_section(self):
        s = ''
        s += "\t.data\n"
        global_symtab = self.parser.all_symtab[0]
        for key, value in sorted(global_symtab.table.items(), key=lambda x: x[1].name):
            if not value.table_ptr:
                # Update this incase float is to be taken as 8 bytes
                s += "global_%s\t.word\t0\n" % value.name
        
        return s

    
    def get_text_section(self):
        s = ''
        s += "\t.text\n"
        global_symtab = self.parser.all_symtab[0]
        for key, value in sorted(global_symtab.table.items(), key=lambda x: x[1].name):
            if value.table_ptr:
                s += "\t.globl %s\n" % value.name
                func_block = self.cfg.blocks[self.cfg.func_to_blocknum[value.name]]
                s += func_block.get_asm(self.parser, self)

        return s

    def __str__(self):
        s = ''
        s += self.get_data_section()
        s += self.get_text_section()

        return s

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

