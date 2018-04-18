
	.data

	.text	# The .text assembler directive indicates
	.globl fn	# The following is the code
fn:
# Prologue begins
	sw $ra, 0($sp)	# Save the return address
	sw $fp, -4($sp)	# Save the frame pointer
	sub $fp, $sp, 8	# Update the frame pointer
	sub $sp, $sp, 16	# Make space for the locals
# Prologue ends
label0:
	lw $s0, 24($sp)
	lw $s1, 0($s0)
	lw $s0, 20($sp)
	sw $s1, 0($s0)
	lw $s0, 32($sp)
	lw $s1, 0($s0)
	lw $s0, 28($sp)
	sw $s1, 0($s0)
	lw $s0, 40($sp)
	lw $s1, 0($s0)
	lw $s0, 36($sp)
	sw $s1, 0($s0)
	j label1
label1:
	j epilogue_fn

# Epilogue begins
epilogue_fn:
	add $sp, $sp, 16
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
	sub $sp, $sp, 32	# Make space for the locals
# Prologue ends
label2:
	lw $s0, 20($sp)
	lw $s1, 0($s0)
	lw $s0, 16($sp)
	sw $s1, 0($s0)
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	lw $s0, 24($sp)
	sw $s1, 0($s0)
	lw $s0, 12($sp)
	lw $s1, 0($s0)
	lw $s0, 8($sp)
	sw $s1, 0($s0)
	j label3
label3:
	j epilogue_main

# Epilogue begins
epilogue_main:
	add $sp, $sp, 32
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends
