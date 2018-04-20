
	.data
global_gf1:	.word	0
global_gf2:	.word	0

	.text	# The .text assembler directive indicates
	.globl floating_arith	# The following is the code
floating_arith:
# Prologue begins
	sw $ra, 0($sp)	# Save the return address
	sw $fp, -4($sp)	# Save the frame pointer
	sub $fp, $sp, 8	# Update the frame pointer
	sub $sp, $sp, 20	# Make space for the locals
# Prologue ends
label0:
	lw $s0, 8($sp)
	lw $s1, 0($s0)
	lw $s0, 12($sp)
	lw $s2, 0($s0)
	add $s0, $s1, $s2
	move $s1, $s0
	lw $s0, 4($sp)
	sw $s1, 0($s0)
	lw $s0, 8($sp)
	lw $s1, 0($s0)
	lw $s0, 12($sp)
	lw $s2, 0($s0)
	sub $s0, $s1, $s2
	move $s1, $s0
	lw $s0, 4($sp)
	sw $s1, 0($s0)
	lw $s0, 8($sp)
	lw $s1, 0($s0)
	lw $s0, 12($sp)
	lw $s2, 0($s0)
	mul $s0, $s1, $s2
	move $s1, $s0
	lw $s0, 4($sp)
	sw $s1, 0($s0)
	lw $s0, 8($sp)
	lw $s1, 0($s0)
	lw $s0, 12($sp)
	lw $s2, 0($s0)
	div $s1, $s2
	mflo $s0
	move $s1, $s0
	lw $s0, 4($sp)
	sw $s1, 0($s0)
	lw $s0, 8($sp)
	lw $s1, 0($s0)
	negu $s0, $s1
	move $s1, $s0
	lw $s0, 4($sp)
	sw $s1, 0($s0)
	la $s0, global_gf1
	sw $s0, 4($sp)
	lw $s0, global_gf2
	sw $s0, 4($sp)
	li $s0, 25
	lw $s1, 4($sp)
	sw $s0, 0($s1)
	j label1
label1:
	j epilogue_floating_arith

# Epilogue begins
epilogue_floating_arith:
	add $sp, $sp, 20
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends
	.text	# The .text assembler directive indicates
	.globl floating_logic	# The following is the code
floating_logic:
# Prologue begins
	sw $ra, 0($sp)	# Save the return address
	sw $fp, -4($sp)	# Save the frame pointer
	sub $fp, $sp, 8	# Update the frame pointer
	sub $sp, $sp, 20	# Make space for the locals
# Prologue ends
label2:
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	lw $s0, 8($sp)
	lw $s2, 0($s0)
	seq $s0, $s1, $s2
	move $s1, $s0
	bne $s1, $0, label3
	j label4
label3:
	li $s0, 2
	lw $s1, 4($sp)
	sw $s0, 0($s1)
	j label14
label4:
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	lw $s0, 8($sp)
	lw $s2, 0($s0)
	slt $s0, $s1, $s2
	move $s1, $s0
	bne $s1, $0, label5
	j label6
label5:
	li $s0, 2
	lw $s1, 4($sp)
	sw $s0, 0($s1)
	j label14
label6:
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	lw $s0, 8($sp)
	lw $s2, 0($s0)
	slt $s0, $s2, $s1
	move $s1, $s0
	bne $s1, $0, label7
	j label8
label7:
	li $s0, 2
	lw $s1, 4($sp)
	sw $s0, 0($s1)
	j label14
label8:
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	lw $s0, 8($sp)
	lw $s2, 0($s0)
	sne $s0, $s1, $s2
	move $s1, $s0
	bne $s1, $0, label9
	j label10
label9:
	li $s0, 2
	lw $s1, 4($sp)
	sw $s0, 0($s1)
	j label14
label10:
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	lw $s0, 8($sp)
	lw $s2, 0($s0)
	sle $s0, $s2, $s1
	move $s1, $s0
	bne $s1, $0, label11
	j label12
label11:
	li $s0, 2
	lw $s1, 4($sp)
	sw $s0, 0($s1)
	j label14
label12:
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	lw $s0, 8($sp)
	lw $s2, 0($s0)
	sle $s0, $s1, $s2
	move $s1, $s0
	bne $s1, $0, label13
	j label14
label13:
	li $s0, 2
	lw $s1, 4($sp)
	sw $s0, 0($s1)
	j label14
label14:
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	lw $s0, 8($sp)
	lw $s2, 0($s0)
	seq $s0, $s1, $s2
	move $s1, $s0
	lw $s0, 4($sp)
	lw $s2, 0($s0)
	lw $s0, 8($sp)
	lw $s3, 0($s0)
	seq $s0, $s2, $s3
	move $s2, $s0
	or $s0, $s1, $s2
	move $s1, $s0
	bne $s1, $0, label15
	j label16
label15:
	li $s0, 2
	lw $s1, 4($sp)
	sw $s0, 0($s1)
	j label20
label16:
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	lw $s0, 8($sp)
	lw $s2, 0($s0)
	seq $s0, $s1, $s2
	move $s1, $s0
	lw $s0, 4($sp)
	lw $s2, 0($s0)
	lw $s0, 8($sp)
	lw $s3, 0($s0)
	seq $s0, $s2, $s3
	move $s2, $s0
	and $s0, $s1, $s2
	move $s1, $s0
	bne $s1, $0, label17
	j label18
label17:
	li $s0, 2
	lw $s1, 4($sp)
	sw $s0, 0($s1)
	j label20
label18:
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	lw $s0, 8($sp)
	lw $s2, 0($s0)
	seq $s0, $s1, $s2
	move $s1, $s0
	xori $s0, $s1, 1
	move $s1, $s0
	bne $s1, $0, label19
	j label20
label19:
	li $s0, 2
	lw $s1, 4($sp)
	sw $s0, 0($s1)
	j label20
label20:
	j epilogue_floating_logic

# Epilogue begins
epilogue_floating_logic:
	add $sp, $sp, 20
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends
