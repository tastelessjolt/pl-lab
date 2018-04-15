from utils import *
from collections import OrderedDict
import st

class Scope(Enum):
    GLOBAL = 0
    LOCAL = 1
    ARGUMENT = 2
    NA = 3

class TableEntry(object):
    def __init__(self, name, type, scope, table_ptr=None, lineno=-1, definition=False):
        self.name = name
        self.type = type
        self.scope = scope
        self.table_ptr = table_ptr
        self.lineno = lineno
        self.definition = definition
        self._offset = 0
        if self.table_ptr:
            self.width = 0
        else:
            self.width = self.type.width
        self.enclosing_symtab = None
    
    def __str__(self, fname='global'):
        if self.table_ptr:
            return '%s\t\t|\t%s\t\t|\t%s' % (self.name, str(self.type[0]), symbol_list_as_dict(self.type[1], False))
        else:
            return '%s\t\t|\t%s\t|\t%s\t|\t%s' % (self.name, fname, self.type.basetype, '*'*self.type.ptr_depth)
    
    def __repr__(self):
        if self.table_ptr:
            return 'Line %d: %s' % (self.lineno, repr ((self.name, self.type, str(self.scope), self.table_ptr.name)))
        else:
            return 'Line %d: %s' % (self.lineno, repr((self.name, self.type, str(self.scope), self.offset, self.width)))

    def isFuncEntry(self):
        return self.table_ptr is not None

    @property
    def size(self):
        if self.table_ptr:
            return self.table_ptr.width
    
    @property
    def offset(self):
        if self.enclosing_symtab and self.scope == Scope.ARGUMENT:
            return self.enclosing_symtab.argument_width + self.enclosing_symtab.width + 8 - self._offset
        else:
            return self._offset + 4

    @offset.setter
    def offset(self, value):
        self._offset = value


class SymTab(object):
    def __init__(self, name='global', parent=None, parent_func=None):
        self.name = name
        self.table = OrderedDict()
        self.parent = parent
        self.parent_func = parent_func
        self.width = 0
        self.argument_width = 0

    def search(self, key):
        if self.table.__contains__(key):
            return self.table[key]
        elif self.parent is not None:
            return self.parent.search(key)
    
    def insert(self, entry_or_entrys):
        if isinstance(entry_or_entrys, list):
            entrys = entry_or_entrys
        else:
            entrys = [entry_or_entrys]
        
        errors = []

        for entry in entrys:
            if not self.table.__contains__(entry.name):
                self.table[entry.name] = entry
                entry.enclosing_symtab = self
                if entry.scope == Scope.LOCAL:
                    entry.offset = self.width
                    self.width += entry.width
                elif entry.scope == Scope.ARGUMENT:
                    entry.offset = self.argument_width
                    self.argument_width += entry.width
            else:
                errors.append(entry)
        if len(errors) > 0:
            raise Exception(errors)
        return entrys

    def insert_replace(self, entry):
        self.table[entry.name] = entry

    def insert_if_same_type(self, entry):
        if self.table.__contains__(entry.name):
            old_entry = self.table[entry.name]
            if old_entry.definition:
                return
            entry_type = old_entry.type
            ins_type = entry.type
            if entry_type == ins_type:
                if not entry.definition:
                    return
                self.table[entry.name] = entry
                return entry
        else:
            self.table[entry.name] = entry
            return entry

    def get(self, key):
        if self.table.__contains__(key):
            return self.table[key]

    def __repr__(self):
        return '%s (%s) [%d] {\n%s\n}' % (self.name, self.parent.name if self.parent else '' , self.width, inc_tabsize('\n'.join([repr(self.table[key]) for key in self.table])))
