Generating LALR tables
Successfully Parsed
ASGN
(
	DEREF
	(
		VAR(a)
	)
	,
	CONST(5)
)

ASGN
(
	DEREF
	(
		VAR(b)
	)
	,
	UMINUS
	(
		VAR(a)
	)
)

ASGN
(
	DEREF
	(
		VAR(d)
	)
	,
	PLUS
	(
		DEREF
		(
			VAR(a)
		)
		,
		CONST(2)
	)
)

ASGN
(
	DEREF
	(
		VAR(c)
	)
	,
	PLUS
	(
		DEREF
		(
			VAR(a)
		)
		,
		DEREF
		(
			VAR(b)
		)
	)
)

ASGN
(
	DEREF
	(
		VAR(c)
	)
	,
	MINUS
	(
		DEREF
		(
			VAR(a)
		)
		,
		DEREF
		(
			VAR(b)
		)
	)
)

ASGN
(
	DEREF
	(
		VAR(c)
	)
	,
	MUL
	(
		DEREF
		(
			VAR(a)
		)
		,
		DEREF
		(
			VAR(b)
		)
	)
)

ASGN
(
	DEREF
	(
		VAR(c)
	)
	,
	DIV
	(
		DEREF
		(
			VAR(a)
		)
		,
		DEREF
		(
			VAR(b)
		)
	)
)
