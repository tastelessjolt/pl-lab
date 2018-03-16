from utils import *
from collections import OrderedDict

class Scope(Enum):
	GLOBAL = 0
	LOCAL = 1
	ARGUMENT = 2

class TableEntry(object):
    def __init__(self, name, type, scope, table_ptr=None):
        self.name = name
        self.type = type
        self.scope = scope
        self.table_ptr = table_ptr
    
    def __repr__(self):
        return repr ((self.name, self.type, self.scope, self.table_ptr))

class SymTab(object):
    def __init__(self, name='__global__'):
        self.name = name
        self.table = OrderedDict()
    
    def insert(self, entry):
        if not self.table.__contains__(entry.name):
            self.table[entry.name] = entry
            return entry

    def insert_replace(self, entry):
        self.table[entry.name] = entry

    def insert_if_same_type(self, entry):
        if self.table.__contains__(entry.name):
            entry_type = self.table[entry.name].type
            ins_type = entry.type
            if entry_type == ins_type:
                self.table[entry.name] = entry
                return entry
        else:
            self.table[entry.name] = entry
            return entry

    def get(self, key):
        if self.table.__contains__(key):
            return self.table[key]

    def __repr__(self):
        return self.name + '\n' + inc_tabsize('\n'.join([ repr (self.table[key]) for key in self.table]))
            
         
