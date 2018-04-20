
	.data

	.text	# The .text assembler directive indicates
	.globl m	# The following is the code
m:
# Prologue begins
	sw $ra, 0($sp)	# Save the return address
	sw $fp, -4($sp)	# Save the frame pointer
	sub $fp, $sp, 8	# Update the frame pointer
	sub $sp, $sp, 16	# Make space for the locals
# Prologue ends
label0:
	lw $s0, 8($sp)
	lw $s1, 4($sp)
	lw $s2, 0($s1)
	sw $s0, 0($s2)
	j label1
label1:
	j epilogue_m

# Epilogue begins
epilogue_m:
	add $sp, $sp, 16
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends
