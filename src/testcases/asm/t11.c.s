
	.data
global_gl:	.space	8
global_pt:	.word	0

	.text	# The .text assembler directive indicates
	.globl f	# The following is the code
f:
# Prologue begins
	sw $ra, 0($sp)	# Save the return address
	sw $fp, -4($sp)	# Save the frame pointer
	sub $fp, $sp, 8	# Update the frame pointer
	sub $sp, $sp, 20	# Make space for the locals
# Prologue ends
label0:
	addi $s0, $sp, 12
	sw $s0, 4($sp)
	lw $s0, 36($sp)
	sw $s0, 24($sp)
	j label1
label1:
	lw $s0, global_pt
	l.s $f10, 0($s0)
	mov.s $f12, $f10
	mov.s $f0, $f12 # move return value to $f0
	j epilogue_f

# Epilogue begins
epilogue_f:
	add $sp, $sp, 20
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends
	.text	# The .text assembler directive indicates
	.globl main	# The following is the code
main:
# Prologue begins
	sw $ra, 0($sp)	# Save the return address
	sw $fp, -4($sp)	# Save the frame pointer
	sub $fp, $sp, 8	# Update the frame pointer
	sub $sp, $sp, 12	# Make space for the locals
# Prologue ends
label2:
	la $s0, global_gl
	sw $s0, global_pt
	# setting up activation record for called function
	lw $s0, 4($sp)
	sw $s0, -20($sp)
	lw $s0, global_pt
	l.s $f10, 0($s0)
	s.s $f10, -12($sp)
	lw $s0, 4($sp)
	sw $s0, -8($sp)
	lw $s0, 4($sp)
	sw $s0, -4($sp)
	lw $s0, 4($sp)
	sw $s0, 0($sp)
	sub $sp, $sp, 24
	jal f # function call
	add $sp, $sp, 24 # destroying activation record of called function
	mov.s $f10, $f0 # using the return value of called function
	lw $s0, global_pt
	s.s $f10, 0($s0)
	j label3
label3:
	j epilogue_main

# Epilogue begins
epilogue_main:
	add $sp, $sp, 12
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends
