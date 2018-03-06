from __future__ import print_function
import sys
from enum import Enum

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def inc_tabsize(string):
	return '\t' + string.replace('\n', '\n\t')

class DataType(object):
	pass

class IntType(DataType):
	# `int**` has ptr_depth = 2; `int` has ptr_depth = 0
	def __init__(self, ptr_depth):
		self.basetype = 'int'
		self.ptr_depth = ptr_depth
	
	def __add__(self, other):
		self.ptr_depth += other
		return self

	def __str__(self):
		return self.basetype + '*'*self.ptr_depth

	def __repr__(self):
		return self.__str__()

class VoidType(DataType):
	def __init__(self):
		self.basetype = 'void'

	def __str__(self):
		return self.basetype
	
	def __repr__(self):
		return self.__str__()

class Operator(Enum):
	plus = 0
	minus = 1
	uminus = 2
	equal = 3
	mul = 4
	divide = 5
	cmp_eq = 6
	cmp_not_eq = 7
	less = 8
	greater = 9
	less_or_eq = 10
	greater_or_eq = 11
	ref = 12
	ptr = 13
	logical_and = 14
	logical_or = 15
	logical_not = 16

	@classmethod
	def arith_sym_to_op(cls, sym):
		return {
			'+': cls.plus,
			'-': cls.minus,
			'*': cls.mul,
			'/': cls.divide,
			'==': cls.cmp_eq,
			'!=': cls.cmp_not_eq,
			'<': cls.less,
			'>': cls.greater,
			'<=': cls.less_or_eq,
			'>=': cls.greater_or_eq,
			'|': cls.logical_or,
			'!': cls.logical_not,
		}[sym]

	def __str__(self):
		try:
			return {
				self.__class__.plus.value: 'PLUS',
				self.__class__.minus.value: 'MINUS',
				self.__class__.uminus.value: 'UMINUS',
				self.__class__.equal.value: 'ASGN',
				self.__class__.mul.value: 'MUL',
				self.__class__.divide.value: 'DIV',
				self.__class__.ref.value: 'ADDR',
				self.__class__.ptr.value: 'DEREF',
				self.__class__.cmp_eq.value: 'DOUBLE_EQUAL',
				self.__class__.cmp_not_eq.value: 'NOT_EQUAL',
				self.__class__.less.value: 'LESS_THAN',
				self.__class__.greater.value: 'GREATER_THAN',
				self.__class__.less_or_eq.value: 'LESS_EQUAL',
				self.__class__.greater_or_eq.value: 'GREATER_EQUAL',
			}[self.value]
		except Exception as e:
			import pdb; pdb.set_trace()
			print (e)

	def __repr__(self):
		return {
			self.__class__.plus.value: '+',
			self.__class__.minus.value: '-',
			self.__class__.uminus.value: '-',
			self.__class__.equal.value: '=',
			self.__class__.mul.value: '*',
			self.__class__.divide.value: '/',
			self.__class__.ref.value: '&',
			self.__class__.ptr.value: '*',
			self.__class__.cmp_eq.value: '==',
			self.__class__.cmp_not_eq.value: '!=',
			self.__class__.less.value: '<',
			self.__class__.greater.value: '>',
			self.__class__.less_or_eq.value: '<=',
			self.__class__.greater_or_eq.value: '>=',
			self.__class__.logical_or.value: '|',
			self.__class__.logical_and.value: '&',
			self.__class__.logical_not.value: '!',
		}[self.value]
