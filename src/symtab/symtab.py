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
    def __init__(self):
        self.table = OrderedDict()
    
    def insert(self, entry):
        if not self.table.__contains__(entry.name):
            self.table[entry.name] = entry
            return True
        else:
            return False

    def __repr__(self):
        return '\n'.join([ repr (self.table[key]) for key in self.table])
            
         
