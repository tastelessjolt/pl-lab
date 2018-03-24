from __future__ import print_function
import sys
from enum import Enum

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def inc_tabsize(string):
	return '\t' + string.replace('\n', '\n\t')

def symbol_list_as_dict(params):
	return '{%s}' % (', '.join(['\'%s\': \'%s\'' % (param.label, param.datatype) if hasattr(param, 'label') else '\'%s\'' % str(param) for param in params]))

class DataType(object):
	def __init__(self):
		self.ptr_depth = 0
	
	def __add__(self, other):
		self.ptr_depth += other
		return self

	def __str__(self):
		return str(self.ptr_depth)

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return ((other.__class__ == self.__class__) and (other.ptr_depth == self.ptr_depth)) or \
                    ( (not issubclass(type(other), DataType)) and other == self)

class IntType(DataType):
	# `int**` has ptr_depth = 2; `int` has ptr_depth = 0
	def __init__(self, ptr_depth_or_datatype):
		self.basetype = 'int'
		if isinstance(ptr_depth_or_datatype, int):
			self.ptr_depth = ptr_depth_or_datatype
		elif isinstance(ptr_depth_or_datatype, DataType):
			self.ptr_depth = ptr_depth_or_datatype.ptr_depth

	def __add__(self, other):
		self.ptr_depth += other
		return self

	def __str__(self):
		return self.basetype + '*'*self.ptr_depth

	def __repr__(self):
		return self.__str__()
	

class FloatType(DataType):
	def __init__(self, ptr_depth_or_datatype):
		self.basetype = 'float'
		if isinstance(ptr_depth_or_datatype, int):
			self.ptr_depth = ptr_depth_or_datatype
		elif isinstance(ptr_depth_or_datatype, DataType):
			self.ptr_depth = ptr_depth_or_datatype.ptr_depth

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


class BooleanType(DataType):
	def __init__(self):
		self.basetype = 'bool'
		self.ptr_depth = 0

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
	logical_and = 12
	logical_or = 13
	logical_not = 14
	ref = 15
	ptr = 16

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
			'||': cls.logical_or,
			'&&': cls.logical_and,
			'!': cls.logical_not,
		}[sym]

	def _is_arithmetic_op(self):
		return self.value >= 0 and self.value <= 5

	def _is_logical_op(self):
		return self.value >= 6 and self.value <= 14

	def _is_reference_op(self):
		return self.value == 15 or self.value == 16

	def __str__(self):
			return {
				self.__class__.plus.value: 'PLUS',
				self.__class__.minus.value: 'MINUS',
				self.__class__.uminus.value: 'UMINUS',
				self.__class__.equal.value: 'ASGN',
				self.__class__.mul.value: 'MUL',
				self.__class__.divide.value: 'DIV',
				self.__class__.ref.value: 'ADDR',
				self.__class__.ptr.value: 'DEREF',
				self.__class__.cmp_eq.value: 'EQ',
				self.__class__.cmp_not_eq.value: 'NE',
				self.__class__.less.value: 'LT',
				self.__class__.greater.value: 'GT',
				self.__class__.less_or_eq.value: 'LE',
				self.__class__.greater_or_eq.value: 'GE',
				self.__class__.logical_and.value: 'AND',
				self.__class__.logical_or.value: 'OR',
				self.__class__.logical_not.value: 'NOT'
			}[self.value]

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
			self.__class__.logical_or.value: '||',
			self.__class__.logical_and.value: '&&',
			self.__class__.logical_not.value: '!',
		}[self.value]

class APLException(Exception):
	pass
