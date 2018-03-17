from utils import *
from collections import OrderedDict

class Scope(Enum):
    GLOBAL = 0
    LOCAL = 1
    ARGUMENT = 2
    NA = 3

class TableEntry(object):
    def __init__(self, name, type, scope, table_ptr=None):
        self.name = name
        self.type = type
        self.scope = scope
        self.table_ptr = table_ptr
    
    def __repr__(self):
        if self.table_ptr:
            return repr ((self.name, self.type, str(self.scope), self.table_ptr.name))
        else:
            return repr((self.name, self.type, str(self.scope)))

class SymTab(object):
    def __init__(self, name='global'):
        self.name = name
        self.table = OrderedDict()

    @classmethod
    def from_stlist(cls, stlist, scope=Scope.NA, name='new'):
        scopes = []
        symtab = cls(name=name)
        for stmt in stlist:
            # TODO: check error handling here 
            tupl = stmt.tableEntry(scope)
            if tupl:
                tmp_tabEntry, tmp_scopes = tupl
                symtab.insert(tmp_tabEntry)
                scopes.extend(tmp_scopes)
        
        if len(symtab.table) != 0:
            return [symtab] + scopes
    
    def insert(self, entry_or_entrys):
        if isinstance(entry_or_entrys, list):
            entrys = entry_or_entrys
        else:
            entrys = [entry_or_entrys]
        for entry in entrys:
            if not self.table.__contains__(entry.name):
                self.table[entry.name] = entry
            else:
                return None
        return entrys

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
            
         
