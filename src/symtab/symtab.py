from utils import *


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

class SymTab(object):
    def __init__(self, entry):
        self.table = {entry.name: entry}
    
    def append(self, entry):
        self.table[entry.name] = entry
         
