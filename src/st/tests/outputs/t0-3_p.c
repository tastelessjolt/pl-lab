Generating LALR tables
Successfully Parsed
ASGN
(
	VAR(pa)
	,
	ADDR
	(
		VAR(a)
	)
)

ASGN
(
	VAR(pb)
	,
	ADDR
	(
		VAR(b)
	)
)

ASGN
(
	VAR(pc)
	,
	ADDR
	(
		VAR(c)
	)
)

ASGN
(
	DEREF
	(
		VAR(pa)
	)
	,
	CONST(2)
)

ASGN
(
	DEREF
	(
		VAR(pb)
	)
	,
	CONST(4)
)

ASGN
(
	DEREF
	(
		VAR(pc)
	)
	,
	DIV
	(
		MUL
		(
			DEREF
			(
				VAR(pa)
			)
			,
			DEREF
			(
				VAR(pb)
			)
		)
		,
		UMINUS
		(
			DEREF
			(
				DEREF
				(
					VAR(pa)
				)
			)
		)
	)
)

