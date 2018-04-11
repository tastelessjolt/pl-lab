from __future__ import print_function
import sys
from enum import Enum

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def inc_tabsize(string):
    return '\t' + string.replace('\n', '\n\t')

def symbol_list_as_dict(params, bracket=True):
    if bracket:
        return '(%s)' % (', '.join(['%s %s' % (param.datatype, param.label) if hasattr(param, 'label') else '%s' % str(param) for param in params]))
    else:
        return '%s' % (', '.join(['%s %s' % (param.datatype, param.label) if hasattr(param, 'label') else '%s' % str(param) for param in params]))

def _super(obj):
    return super(type(obj), obj)

def symtab_from_ast(parser, ast):
    # s = '\n'.join([repr(symtab) for symtab in parser.all_symtab]) + "\n"
    s = ''
    s += 'Procedure table :-\n'
    s += '-----------------------------------------------------------------\n'
    s += 'Name\t\t|\tReturn Type  |  Parameter List\n'
    for key, value in sorted(parser.all_symtab[0].table.items(), key=lambda x: x[1].name):
        if value.table_ptr and value.name != 'main':
                s += str(value) + "\n"
    s += '-----------------------------------------------------------------\n'
    s += 'Variable table :-\n'
    s += '-----------------------------------------------------------------\n'
    s += 'Name\t|\tScope\t\t|\tBase Type  |  Derived Type\n'
    s += '-----------------------------------------------------------------\n'
    all_symtab_copy = parser.all_symtab[1:]
    all_symtab_copy.reverse()
    all_symtab_copy.insert(0, parser.all_symtab[0])
    for symtab in sorted(all_symtab_copy, key=lambda  x: x.name):
        for key, value in sorted(symtab.table.items(), key=lambda x: x[1].name):
            if not value.table_ptr:
                s += value.__str__('procedure ' + str(symtab.name)
                                    if symtab.name != 'global' else 'global') + "\n"
    s += '-----------------------------------------------------------------\n'
    s += '-----------------------------------------------------------------\n'
    return s

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
        return '*'*self.ptr_depth + self.basetype

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
        return '*'*self.ptr_depth + self.basetype

    def __repr__(self):
        return self.__str__()

class VoidType(DataType):
    def __init__(self):
        self.basetype = 'void'

    def __str__(self):
        return self.basetype
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, VoidType)


class BooleanType(DataType):
    def __init__(self):
        self.basetype = 'bool'
        self.ptr_depth = 0

    def __str__(self):
        return self.basetype
    
    def __repr__(self):
        return self.__str__()

class AnyType(DataType):
    def __init__(self):
        self.basetype = 'nothing'

    def __eq__(self, other):
        return issubclass(type(other), DataType)

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


class Register(Enum):
# General Purpose registers
    zero = 0
    at = 1
    v0 = 2
    v1 = 3
    a0 = 4
    a1 = 5
    a2 = 6
    a3 = 7
    t0 = 8
    t1 = 9
    t2 = 10
    t3 = 11
    t4 = 12
    t5 = 13
    t6 = 14
    t7 = 15
    s0 = 16
    s1 = 17
    s2 = 18
    s3 = 19
    s4 = 20
    s5 = 21
    s6 = 22
    s7 = 23
    t8 = 24
    t9 = 25
    k0 = 26
    k1 = 27
    gp = 28
    sp = 29
    fp = 30
    ra = 31
# Floating Point registers
    f0 = 32
    f1 = 33
    f2 = 34
    f3 = 35
    f4 = 36
    f5 = 37
    f6 = 38
    f7 = 39
    f8 = 40
    f9 = 41
    f10 = 42
    f11 = 43
    f12 = 44
    f13 = 45
    f14 = 46
    f15 = 47
    f16 = 48
    f17 = 49
    f18 = 50
    f19 = 51
    f20 = 52
    f21 = 53
    f22 = 54
    f23 = 55
    f24 = 56
    f25 = 57
    f26 = 58
    f27 = 59
    f28 = 60
    f29 = 61
    f30 = 62
    f31 = 63

    def __str__(self):
        return '$' + self.name

