
	.data
global_gf1:	.space	8
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
	l.s $f10, 0($s0)
	lw $s0, 12($sp)
	l.s $f12, 0($s0)
	add.s $f14, $f10, $f12
	mov.s $f10, $f14
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
	lw $s0, 8($sp)
	l.s $f10, 0($s0)
	lw $s0, 12($sp)
	l.s $f12, 0($s0)
	sub.s $f14, $f10, $f12
	mov.s $f10, $f14
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
	lw $s0, 8($sp)
	l.s $f10, 0($s0)
	lw $s0, 12($sp)
	l.s $f12, 0($s0)
	mul.s $f14, $f10, $f12
	mov.s $f10, $f14
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
	lw $s0, 8($sp)
	l.s $f10, 0($s0)
	lw $s0, 12($sp)
	l.s $f12, 0($s0)
	div.s $f14, $f10, $f12
	mov.s $f10, $f14
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
	lw $s0, 8($sp)
	l.s $f10, 0($s0)
	neg.s $f12, $f10
	mov.s $f10, $f12
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
	la $s0, global_gf1
	sw $s0, 4($sp)
	lw $s0, global_gf2
	sw $s0, 4($sp)
	li.s $f10, 2.5
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
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
	l.s $f10, 0($s0)
	lw $s0, 8($sp)
	l.s $f12, 0($s0)
	c.eq.s $f10, $f12
	bc1f L_CondFalse_0
	li $s0, 1
	j L_CondEnd_0
L_CondFalse_0:
	li $s0, 0
L_CondEnd_0:
	move $s1, $s0
	bne $s1, $0, label3
	j label4
label3:
	li.s $f10, 2.0
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
	j label14
label4:
	lw $s0, 4($sp)
	l.s $f10, 0($s0)
	lw $s0, 8($sp)
	l.s $f12, 0($s0)
	c.lt.s $f10, $f12
	bc1f L_CondFalse_1
	li $s0, 1
	j L_CondEnd_1
L_CondFalse_1:
	li $s0, 0
L_CondEnd_1:
	move $s1, $s0
	bne $s1, $0, label5
	j label6
label5:
	li.s $f10, 2.0
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
	j label14
label6:
	lw $s0, 4($sp)
	l.s $f10, 0($s0)
	lw $s0, 8($sp)
	l.s $f12, 0($s0)
	c.lt.s $f12, $f10
	bc1f L_CondFalse_2
	li $s0, 1
	j L_CondEnd_2
L_CondFalse_2:
	li $s0, 0
L_CondEnd_2:
	move $s1, $s0
	bne $s1, $0, label7
	j label8
label7:
	li.s $f10, 2.0
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
	j label14
label8:
	lw $s0, 4($sp)
	l.s $f10, 0($s0)
	lw $s0, 8($sp)
	l.s $f12, 0($s0)
	c.eq.s $f10, $f12
	bc1f L_CondTrue_3
	li $s0, 0
	j L_CondEnd_3
L_CondTrue_3:
	li $s0, 1
L_CondEnd_3:
	move $s1, $s0
	bne $s1, $0, label9
	j label10
label9:
	li.s $f10, 2.0
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
	j label14
label10:
	lw $s0, 4($sp)
	l.s $f10, 0($s0)
	lw $s0, 8($sp)
	l.s $f12, 0($s0)
	c.le.s $f12, $f10
	bc1f L_CondFalse_4
	li $s0, 1
	j L_CondEnd_4
L_CondFalse_4:
	li $s0, 0
L_CondEnd_4:
	move $s1, $s0
	bne $s1, $0, label11
	j label12
label11:
	li.s $f10, 2.0
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
	j label14
label12:
	lw $s0, 4($sp)
	l.s $f10, 0($s0)
	lw $s0, 8($sp)
	l.s $f12, 0($s0)
	c.le.s $f10, $f12
	bc1f L_CondFalse_5
	li $s0, 1
	j L_CondEnd_5
L_CondFalse_5:
	li $s0, 0
L_CondEnd_5:
	move $s1, $s0
	bne $s1, $0, label13
	j label14
label13:
	li.s $f10, 2.0
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
	j label14
label14:
	lw $s0, 4($sp)
	l.s $f10, 0($s0)
	lw $s0, 8($sp)
	l.s $f12, 0($s0)
	c.eq.s $f10, $f12
	bc1f L_CondFalse_6
	li $s0, 1
	j L_CondEnd_6
L_CondFalse_6:
	li $s0, 0
L_CondEnd_6:
	move $s1, $s0
	lw $s0, 4($sp)
	l.s $f10, 0($s0)
	lw $s0, 8($sp)
	l.s $f12, 0($s0)
	c.eq.s $f10, $f12
	bc1f L_CondFalse_7
	li $s0, 1
	j L_CondEnd_7
L_CondFalse_7:
	li $s0, 0
L_CondEnd_7:
	move $s2, $s0
	or $s0, $s1, $s2
	move $s1, $s0
	bne $s1, $0, label15
	j label16
label15:
	li.s $f10, 2.0
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
	j label20
label16:
	lw $s0, 4($sp)
	l.s $f10, 0($s0)
	lw $s0, 8($sp)
	l.s $f12, 0($s0)
	c.eq.s $f10, $f12
	bc1f L_CondFalse_8
	li $s0, 1
	j L_CondEnd_8
L_CondFalse_8:
	li $s0, 0
L_CondEnd_8:
	move $s1, $s0
	lw $s0, 4($sp)
	l.s $f10, 0($s0)
	lw $s0, 8($sp)
	l.s $f12, 0($s0)
	c.eq.s $f10, $f12
	bc1f L_CondFalse_9
	li $s0, 1
	j L_CondEnd_9
L_CondFalse_9:
	li $s0, 0
L_CondEnd_9:
	move $s2, $s0
	and $s0, $s1, $s2
	move $s1, $s0
	bne $s1, $0, label17
	j label18
label17:
	li.s $f10, 2.0
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
	j label20
label18:
	lw $s0, 4($sp)
	l.s $f10, 0($s0)
	lw $s0, 8($sp)
	l.s $f12, 0($s0)
	c.eq.s $f10, $f12
	bc1f L_CondFalse_10
	li $s0, 1
	j L_CondEnd_10
L_CondFalse_10:
	li $s0, 0
L_CondEnd_10:
	move $s1, $s0
	xori $s0, $s1, 1
	move $s1, $s0
	bne $s1, $0, label19
	j label20
label19:
	li.s $f10, 2.0
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
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
