Generating LALR tables
Successfully Parsed




ASGN
(
	DEREF
	(
		VAR(px)
	)
	,
	CONST(5)
)
ASGN
(
	DEREF
	(
		VAR(y)
	)
	,
	PLUS
	(
		PLUS
		(
			CONST(1)
			,
			CONST(2)
		)
		,
		CONST(3)
	)
)
ASGN
(
	DEREF
	(
		VAR(pz)
	)
	,
	CONST(1)
)
ASGN
(
	DEREF
	(
		VAR(z)
	)
	,
	MINUS
	(
		PLUS
		(
			DEREF
			(
				DEREF
			(
				VAR(px)
			)
			)
			,
			DEREF
			(
				VAR(py)
			)
		)
		,
		DEREF
		(
			DEREF
		(
			DEREF
		(
			VAR(px)
		)
		)
		)
	)
)
ASGN
(
	VAR(sdasz)
	,
	PLUS
	(
		MUL
		(
			UMINUS
			(
				DEREF
			(
				VAR(z)
			)
			)
			,
			ADDR
			(
				VAR(y)
			)
		)
		,
		DEREF
		(
			VAR(x)
		)
	)
)


