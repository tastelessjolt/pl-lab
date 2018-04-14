from utils import *

all_instructions = []

class ASM:
    pass

class SPIM(ASM):
    def __init__(self, parser, cfg):
        self.cfg = cfg
        self.parser = parser
        self.instructions = all_instructions
        self.free_registers = Stack()
        self.var_to_reg_map = {}

    def get_register(self, var):
        if self.var_to_reg_map.__contains__(var.label):
            return self.var_to_reg_map[var.label]
        else:
            raise NotImplementedError

    def set_register(self, var, reg):
        self.var_to_reg_map[var.label] = reg

    def new_register(self):
        if self.free_registers.isEmpty():
            eprint("Out of registers!")
            eprint("Exiting...")
            sys.exit()
        else:
            return self.free_registers.pop()

    def free_register(self, *regs):
        for reg in regs:
            self.free_registers.push(reg)

    def get_data_section(self):
        s = ''
        s += "\t.data\n"
        global_symtab = self.parser.all_symtab[0]
        for key, value in sorted(global_symtab.table.items(), key=lambda x: x[1].name):
            if not value.table_ptr:
                # Update this incase float is to be taken as 8 bytes
                if value.type.isFloat():
                    s += "global_%s\t.space\t%d\n" % (value.name, value.width)
                else:
                    s += "global_%s\t.word\t0\n" % value.name
        
        return s

    def get_prologue(self, func_entry):
        s = ''
        s += 'sw $ra, 0($sp)  # Save the return address\n'
        s += 'sw $fp, -4($sp) # Save the frame pointer\n'
        s += 'sub $fp, $sp, 8 # Update the frame pointer\n'
        s += 'sub $sp, $sp, %d    # Make space for the locals\n' % (func_entry.size + 8)
        return s
    
    def get_epilogue(self, func_entry):
        s = ''
        s += '# Epilogue begins'
    
    def get_text_section(self):
        s = ''
        global_symtab = self.parser.all_symtab[0]
        for key, value in sorted(global_symtab.table.items(), key=lambda x: x[1].name):
            if value.table_ptr:
                s += "\t.text\n"
                s += "\t.globl %s\n%s:\n" % (value.name, value.name)
                s += "# Prologue begins\n"
                s += inc_tabsize(self.get_prologue(value))
                s += "# Prologue ends\n"
                func_block = self.cfg.blocks[self.cfg.func_to_blocknum[value.name]]
                s += func_block.get_asm(self.parser, self)
                s += "# Epilogue begins\n"
                s += "epilogue_%s:\n" % value.name
                s += inc_tabsize(self.get_epilogue(value))
                s += "# Epilogue ends\n"

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
        mysuper(self).__init__(opcode, operands)

class IInstruction(Instruction):
    def __init__(self, opcode, operands):
        mysuper(self).__init__(opcode, operands)

class JInstruction(Instruction):
    def __init__(self, opcode, operands):
        mysuper(self).__init__(opcode, operands)

