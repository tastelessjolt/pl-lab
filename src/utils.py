from __future__ import print_function
import sys
from enum import Enum

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Operator(Enum):
	plus = 0
	minus = 1
	uminus = 2
	equal = 3
	mul = 4
	divide = 5
	ref = 6
	ptr = 7

	@classmethod
	def arith_sym_to_op(cls, sym):
		return {
			'+': cls.plus,
			'-': cls.minus,
			'*': cls.mul,
			'/': cls.divide,
		}[sym]

	def __str__(self):
		return {
			0: 'PLUS',
			1: 'MINUS',
			2: 'UMINUS',
			3: 'ASGN',
			4: 'MUL',
			5: 'DIV',
			6: 'ADDR',
			7: 'DEREF',
		}[self.value]