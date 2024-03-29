from utils import *

all_instructions = []

class ASM:
    pass

class SPIM(ASM):
    def __init__(self, parser, cfg):
        self.cfg = cfg
        self.parser = parser
        self.instructions = all_instructions
        self.free_registers = RegStack()
        self.var_to_reg_map = {}
        self.code = []
        self.fp_j_label = 0

    def get_register(self, var, symtab):
        if var in self.var_to_reg_map:
            return self.var_to_reg_map[var]
        else:
            symtabEntry = symtab.search(var.label)
            if symtabEntry and not symtabEntry.isFuncEntry():
                reg = self.set_register(var)
                self.code.append(Instruction(InstrOp.lw, reg, symtabEntry.offset, Register.sp))
                return reg
            else:
                return self.set_register(var)
                # raise Exception ('Variable %s not found in the symtab or in the temporaries' % var.label )

    def free_variable(self, var):
        self._free_register(self.var_to_reg_map.pop(var, None))

    def set_register(self, ast):
        reg = self._new_register(ast.type)
        self.var_to_reg_map[ast] = reg
        return reg

    def _set_reg(self, ast, reg):
        self.var_to_reg_map[ast] = reg

    def _new_register(self, type):
        if self.free_registers.isEmpty(type):
            eprint("Out of registers!")
            eprint("Exiting...")
            sys.exit()
        else:
            return self.free_registers.pop(type)

    def _free_register(self, *regs):
        for reg in regs:
            if reg is not None:
                self.free_registers.push(reg)

    def get_data_section(self):
        s = ''
        s += "\t.data\n"
        global_symtab = self.parser.all_symtab[0]
        for _, value in sorted(global_symtab.table.items(), key=lambda x: x[1].name):
            if not value.table_ptr:
                # Update this incase float is to be taken as 8 bytes
                if value.type.isFloat():
                    s += "global_%s:\t.space\t%d\n" % (value.name, value.width)
                else:
                    s += "global_%s:\t.word\t0\n" % value.name
        
        return s

    def get_prologue(self, func_entry):
        s = ''
        s += 'sw $ra, 0($sp)  # Save the return address\n'
        s += 'sw $fp, -4($sp) # Save the frame pointer\n'
        s += 'sub $fp, $sp, 8 # Update the frame pointer\n'
        s += 'sub $sp, $sp, %d    # Make space for the locals' % (func_entry.size + 8)
        return s
    
    def get_epilogue(self, func_entry):
        s = ''
        s += 'add $sp, $sp, %d\n' % (func_entry.size + 8)
        s += 'lw $fp, -4($sp)\n'
        s += 'lw $ra, 0($sp)\n'
        s += 'jr $ra  # Jump back to the called procedure'
        return s
    
    def get_text_section(self):
        s = ''


        global_symtab = self.parser.all_symtab[0]
        # for value in global_symtab.table.values():
        #     if value.table_ptr:

        global_list = self.cfg.ast.global_list
        for func in global_list:
            if func.isFunc() and not func.declaration:
                value = global_symtab.search(func.fname)
                if value is None:
                    raise Exception('Not found %s function in symtab')
                s += "\t.text\t# The .text assembler directive indicates\n"
                s += "\t.globl %s\t# The following is the code\n" % value.name
                s += "%s:\n" % value.name
                s += "# Prologue begins\n"
                s += inc_tabsize(self.get_prologue(value))
                s += '\n'
                s += "# Prologue ends\n"
                start_block, end_block = self.cfg.func_to_blocknum[value.name]
                for blocknum in range(start_block, end_block):
                    curr_block = self.cfg.blocks[blocknum]
                    curr_block.get_asm(self.parser, value.table_ptr, self)

                s +=  ''.join([ (inc_tabsize(str(inst)) + '\n') if isinstance(inst, Instruction) else str(inst) for inst in self.code])
                self.code.clear()
                s += '\n'
                s += "# Epilogue begins\n"
                s += "epilogue_%s:\n" % value.name
                s += inc_tabsize(self.get_epilogue(value))
                s += '\n'
                s += "# Epilogue ends\n"

        return s

    def __str__(self):
        s = ''
        s += self.get_data_section()
        s += self.get_text_section()

        return s

class InstrOp(Enum):
    add = 0
    sub = 1
    mul = 2
    j = 3
    beq = 4
    bne = 5
    li = 6
    lw = 7
    sw = 8
    sne = 9
    seq = 10
    move = 11
    jal = 12
    jr = 13
    xori = 14
    addi = 15
    _and = 16
    _or = 17
    _not = 18
    slt = 19
    sle = 20
    div = 21
    mflo = 22
    negu = 23
    _ = 24
    add_s = 25
    sub_s = 26
    mul_s = 27
    div_s = 28
    l_s = 29
    li_s = 30
    s_s = 31
    mov_s = 32
    neg_s = 33
    c_eq_s = 34
    c_lt_s = 35
    c_le_s = 36
    bc1t = 37
    bc1f = 38
    la = 39

    def __str__(self):
        return self.name.replace('_', '.') if self.name[0] != '_' else self.name[1:]

class Instruction:
    def __init__(self, operator=InstrOp._, *operands, comment = ''):
        self.operator = operator
        self.operands = operands
        isFloat = False
        for operand in self.operands:
            if isinstance(operand, Register) and operand.is_float:
                isFloat = True

        if isFloat:
            self.operator = Instruction.get_float_form[self.operator]

        self.comment = comment

    get_float_form = {
        InstrOp.add: InstrOp.add_s,
        InstrOp.sub: InstrOp.sub_s,
        InstrOp.mul: InstrOp.mul_s,
        InstrOp.div: InstrOp.div_s,
        InstrOp.lw: InstrOp.l_s,
        InstrOp.li: InstrOp.li_s,
        InstrOp.sw: InstrOp.s_s,
        InstrOp.move: InstrOp.mov_s,
        InstrOp.negu: InstrOp.neg_s,
        InstrOp.seq: InstrOp.c_eq_s,
        InstrOp.slt: InstrOp.c_lt_s,
        InstrOp.sne: InstrOp.c_eq_s,
        InstrOp.sle: InstrOp.c_le_s,
    }


    def _format_sl(self):
        try:
            return '%s %s, %d(%s)' % (self.operator, self.operands[0], self.operands[1], self.operands[2])
        except:
            return repr(self)

    def __str__(self):
        sl = {
            InstrOp.sw: self._format_sl,
            InstrOp.lw: self._format_sl,
            InstrOp.s_s: self._format_sl,
            InstrOp.l_s: self._format_sl,
        }
        func = sl.get (self.operator, None)
        if func:
            return func()

        return repr (self)
        # return str(self.operator) + " ".join([str(reg) for reg in self.operands])

    def __repr__(self):
        s = ''
        if self.operator != InstrOp._:
            return str(self.operator) + ' ' + ', '.join([str(i) for i in self.operands]) + \
            (" # %s" % self.comment if self.comment else "")
        else:
            return "# %s" % self.comment
        

class RInstruction(Instruction):
    def __init__(self, operator, operands):
        mysuper(self).__init__(operator, operands)

class IInstruction(Instruction):
    def __init__(self, operator, operands):
        mysuper(self).__init__(operator, operands)

class JInstruction(Instruction):
    def __init__(self, operator, operands):
        mysuper(self).__init__(operator, operands)

class Directives(Enum):
    data = 0
    text = 1
    globl = 2

class AsmDirectives:
    def __init__(self, directive, *operands):
        self.directive = directive
        self.operands = operands

class Label:
    def __init__(self, name, value = None):
        self.name = name
        self.value = value

    def __repr__(self):
        return self.name + ':' + (self.value if self.value is not None else '') + '\n'

    
