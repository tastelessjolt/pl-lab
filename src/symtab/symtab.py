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
    
    def __repr__(self):
        if self.table_ptr:
            return 'Line %d: %s' % (self.lineno, repr ((self.name, self.type, str(self.scope), self.table_ptr.name)))
        else:
            return 'Line %d: %s' % (self.lineno, repr((self.name, self.type, str(self.scope))))

class SymTab(object):
    def __init__(self, name='global', parent=None):
        self.name = name
        self.table = OrderedDict()
        self.parent = parent

    def search(self, key):
        if self.table.__contains__(key):
            return self.table[key]
        elif self.parent is not None:
            return self.parent.search(key)

    @classmethod
    def from_stlist(cls, stlist, scope=Scope.NA, name='untitled', parent=None, params=[]):
        scopes = []
        symtab = cls(name=name, parent=parent)
        errors = []

        # params are the function params 
        for symbol in params:
            try:
                symtab.insert( symbol.tableEntry(Scope.ARGUMENT) )
            except Exception as e:
                for err_entry in e.args[0]:
                    errors.append('symbol re-declaration at %s: \n\tAlready declared at %s' % (
                        repr(err_entry), repr(symtab.table[err_entry.name])))
        
        for stmt in stlist:
            # TODO: check error handling here 
            tupl = stmt.tableEntry(scope, parent=symtab)
            if tupl:
                tmp_tabEntry, tmp_scopes, t_errors = tupl
                errors.extend(t_errors)
                if isinstance(stmt, st.Func) and not stmt.declaration:
                    if symtab.insert_if_same_type(tmp_tabEntry):
                        scopes.extend(tmp_scopes)
                    else:
                        errors.append('function re-declaration at %s: \n\tAlready declared at %s' % (repr(tmp_tabEntry), repr(symtab.table[tmp_tabEntry.name])))
                else:
                    try:
                        symtab.insert(tmp_tabEntry)
                        scopes.extend(tmp_scopes)
                    except Exception as e:
                        for err_entry in e.args[0]:
                            errors.append('symbol re-declaration at %s: \n\tAlready declared at %s' % (repr(err_entry), repr(symtab.table[err_entry.name])))
        
        if len(symtab.table) != 0:
            return ([symtab] + scopes, errors)
    
    def insert(self, entry_or_entrys):
        if isinstance(entry_or_entrys, list):
            entrys = entry_or_entrys
        else:
            entrys = [entry_or_entrys]
        
        errors = []

        for entry in entrys:
            if not self.table.__contains__(entry.name):
                self.table[entry.name] = entry
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
                self.table[entry.name] = entry
                return entry
        else:
            self.table[entry.name] = entry
            return entry

    def get(self, key):
        if self.table.__contains__(key):
            return self.table[key]

    def __repr__(self):
        return '%s (%s) {\n%s\n}' % (self.name, self.parent.name if self.parent else '' , inc_tabsize('\n'.join([repr(self.table[key]) for key in self.table])))
            
         
