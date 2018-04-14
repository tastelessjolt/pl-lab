from .asm import *

'''
    abs Rdest, Rsrc # Absolute Value
    add Rdest, Rsrc1, Src2 # Addition (with overflow)
    addi Rdest, Rsrc1, Imm # Addition Immediate (with overflow)
    addu Rdest, Rsrc1, Src2 # Addition (without overflow)
    addiu Rdest, Rsrc1, Imm # Addition Immediate (without overflow)
    and Rdest, Rsrc1, Src2 # AND
    andi Rdest, Rsrc1, Imm # AND Immediate
    div Rsrc1, Rsrc2 # Divide (with overflow)
    divu Rsrc1, Rsrc2 # Divide (without overflow)
    div Rdest, Rsrc1, Src2 # Divide (with overflow)
    divu Rdest, Rsrc1, Src2 # Divide (without overflow)
    mul Rdest, Rsrc1, Src2 # Multiply (without overflow)
    mulo Rdest, Rsrc1, Src2 # Multiply (with overflow)
    mulou Rdest, Rsrc1, Src2 # Unsigned Multiply (with overflow)
    mult Rsrc1, Rsrc2 # Multiply
    multu Rsrc1, Rsrc2 # Unsigned Multiply
    neg Rdest, Rsrc # Negate Value (with overflow)
    negu Rdest, Rsrc # Negate Value (without overflow)
    nor Rdest, Rsrc1, Src2 # NOR
    not Rdest, Rsrc # NOT
    or Rdest, Rsrc1, Src2 # OR
    ori Rdest, Rsrc1, Imm # OR Immediate
    rem Rdest, Rsrc1, Src2 # Remainder
    remu Rdest, Rsrc1, Src2 # Unsigned Remainder
    rol Rdest, Rsrc1, Src2 # Rotate Left
    ror Rdest, Rsrc1, Src2 # Rotate Right
    sll Rdest, Rsrc1, Src2 # Shift Left Logical
    sllv Rdest, Rsrc1, Rsrc2 # Shift Left Logical Variable
    sra Rdest, Rsrc1, Src2 # Shift Right Arithmetic
    srav Rdest, Rsrc1, Rsrc2 # Shift Right Arithmetic Variable
    srl Rdest, Rsrc1, Src2 # Shift Right Logical
    srlv Rdest, Rsrc1, Rsrc2 # Shift Right Logical Variable
    sub Rdest, Rsrc1, Src2 # Subtract (with overflow)
    subu Rdest, Rsrc1, Src2 # Subtract (without overflow)
    xor Rdest, Rsrc1, Src2 # XOR
    xori Rdest, Rsrc1, Imm # XOR Immediate
    li Rdest, imm # Load Immediate
    lui Rdest, imm # Load Upper Immediate
    seq Rdest, Rsrc1, Src2 # Set Equal
    sge Rdest, Rsrc1, Src2 # Set Greater Than Equal
    sgeu Rdest, Rsrc1, Src2 # Set Greater Than Equal Unsigned
    sgt Rdest, Rsrc1, Src2 # Set Greater Than
    sgtu Rdest, Rsrc1, Src2 # Set Greater Than Unsigned
    sle Rdest, Rsrc1, Src2 # Set Less Than Equal
    sleu Rdest, Rsrc1, Src2 # Set Less Than Equal Unsigned
    slt Rdest, Rsrc1, Src2 # Set Less Than
    slti Rdest, Rsrc1, Imm # Set Less Than Immediate
    sltu Rdest, Rsrc1, Src2 # Set Less Than Unsigned
    sltiu Rdest, Rsrc1, Imm # Set Less Than Unsigned Immediate
    sne Rdest, Rsrc1, Src2 # Set Not Equal
    b label # Branch instruction
    bczt label # Branch Coprocessor <EM
    bczf label # Branch Coprocessor <EM
    beq Rsrc1, Src2, label # Branch on Equal
    beqz Rsrc, label # Branch on Equal Zero
    bge Rsrc1, Src2, label # Branch on Greater Than Equal
    bgeu Rsrc1, Src2, label # Branch on GTE Unsigned
    bgez Rsrc, label # Branch on Greater Than Equal Zero
    bgezal Rsrc, label # Branch on Greater Than Equal Zero And Link
    bgt Rsrc1, Src2, label # Branch on Greater Than
    bgtu Rsrc1, Src2, label # Branch on Greater Than Unsigned
    bgtz Rsrc, label # Branch on Greater Than Zero
    ble Rsrc1, Src2, label # Branch on Less Than Equal
    bleu Rsrc1, Src2, label # Branch on LTE Unsigned
    blez Rsrc, label # Branch on Less Than Equal Zero
    bgezal Rsrc, label # Branch on Greater Than Equal Zero And Link
    bltzal Rsrc, label # Branch on Less Than And Link
    blt Rsrc1, Src2, label # Branch on Less Than
    bltu Rsrc1, Src2, label # Branch on Less Than Unsigned
    bltz Rsrc, label # Branch on Less Than Zero
    bne Rsrc1, Src2, label # Branch on Not Equal
    bnez Rsrc, label # Branch on Not Equal Zero
    j label # Jump
    jal label # Jump and Link
    jalr Rsrc # Jump and Link Register
    jr Rsrc # Jump Register
    la Rdest, address # Load Address
    lb Rdest, address # Load Byte
    lbu Rdest, address # Load Unsigned Byte
    ld Rdest, address # Load Double-Word
    lh Rdest, address # Load Halfword
    lhu Rdest, address # Load Unsigned Halfword
    lw Rdest, address # Load Word
    lwcz Rdest, address # Load Word Coprocessor <EM
    lwl Rdest, address # Load Word Left
    lwr Rdest, address # Load Word Right
    ulh Rdest, address # Unaligned Load Halfword
    ulhu Rdest, address # Unaligned Load Halfword Unsigned
    ulw Rdest, address # Unaligned Load Word
    sb Rsrc, address # Store Byte
    sd Rsrc, address # Store Double-Word
    sh Rsrc, address # Store Halfword
    sw Rsrc, address # Store Word
    swcz Rsrc, address # Store Word Coprocessor <EM
    swl Rsrc, address # Store Word Left
    swr Rsrc, address # Store Word Right
    ush Rsrc, address # Unaligned Store Halfword
    usw Rsrc, address # Unaligned Store Word
    move Rdest, Rsrc # Move
    mfhi Rdest # Move From hi
    mflo Rdest # Move From lo
    mthi Rdest # Move To hi
    mtlo Rdest # Move To lo
    mfcz Rdest, CPsrc #  Move From Coprocessor <EM
    mfc1.d Rdest, FRsrc1 # Move Double From Coprocessor 1
    mtcz Rsrc, CPdest # Move To Coprocessor <EM
    abs.d FRdest, FRsrc # Floating Point Absolute Value Double
    abs.s FRdest, FRsrc # Floating Point Absolute Value Single
    add.d FRdest, FRsrc1, FRsrc2 # Floating Point Addition Double
    add.s FRdest, FRsrc1, FRsrc2 # Floating Point Addition Single
    c.eq.d FRsrc1, FRsrc2 # Compare Equal Double
    c.eq.s FRsrc1, FRsrc2 # Compare Equal Single
    c.le.d FRsrc1, FRsrc2 # Compare Less Than Equal Double
    c.le.s FRsrc1, FRsrc2 # Compare Less Than Equal Single
    c.lt.d FRsrc1, FRsrc2 # Compare Less Than Double
    c.lt.s FRsrc1, FRsrc2 # Compare Less Than Single
    cvt.d.s FRdest, FRsrc # Convert Single to Double
    cvt.d.w FRdest, FRsrc # Convert Integer to Double
    cvt.s.d FRdest, FRsrc # Convert Double to Single
    cvt.s.w FRdest, FRsrc # Convert Integer to Single
    cvt.w.d FRdest, FRsrc # Convert Double to Integer
    cvt.w.s FRdest, FRsrc # Convert Single to Integer
    div.d FRdest, FRsrc1, FRsrc2 # Floating Point Divide Double
    div.s FRdest, FRsrc1, FRsrc2 # Floating Point Divide Single
    l.d FRdest, address # Load Floating Point Double
    l.s FRdest, address # Load Floating Point Single
    mov.d FRdest, FRsrc # Move Floating Point Double
    mov.s FRdest, FRsrc # Move Floating Point Single
    mul.d FRdest, FRsrc1, FRsrc2 # Floating Point Multiply Double
    mul.s FRdest, FRsrc1, FRsrc2 # Floating Point Multiply Single
    neg.d FRdest, FRsrc # Negate Double
    neg.s FRdest, FRsrc # Negate Single
    s.d FRdest, address # Store Floating Point Double
    s.s FRdest, address # Store Floating Point Single
    sub.d FRdest, FRsrc1, FRsrc2 # Floating Point Subtract Double
    sub.s FRdest, FRsrc1, FRsrc2 # Floating Point Subtract Single
    rfe # Return From Exception
    syscall # System Call
    break n # Break
    nop # No operation
'''

r_instructions = []
i_instructions = []
j_instructions = []
misc_instructions = []