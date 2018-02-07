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

	def __str__(self):
		return {
			0: '+',
			1: '-',
			2: '-',
			3: '=',
			4: '*',
			5: '/',
		}[self.value]