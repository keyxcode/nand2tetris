from typing import Literal, Optional

_SymbolKind = Literal["static", "field", "arg", "var"]

class SymbolTable:
    def __init__(self):
        self.class_symbols = dict()
        self.method_symbols = dict()

        self.static_idx = 0
        self.field_idx = 0
        self.arg_idx = 0
        self.var_idx = 0

    def start_subroutine(self) -> None:
        self.method_symbols.clear()
        self.arg_idx = 0
        self.var_idx = 0

    def define(self, name: str, type: str, kind: _SymbolKind) -> None:
        if kind in ("static", "field"):
            self.class_symbols[name] = (type, kind, self.get_and_increment_idx(kind))
        elif kind in ("arg", "var"):
            self.method_symbols[name] = (type, kind, self.get_and_increment_idx(kind))

    def get_and_increment_idx(self, kind: _SymbolKind) -> int:
        if kind == "static":
            res = self.static_idx
            self.static_idx += 1
        elif kind == "field":
            res = self.field_idx
            self.field_idx += 1
        elif kind == "arg":
            res = self.arg_idx
            self.arg_idx += 1
        else: # var
            res = self.var_idx
            self.var_idx += 1
        
        return res

    # def var_count(self, kind: SymbolKind) -> int:
    #     pass

    def get_type_of(self, name: str) -> str:
        return self.get_symbol_info(name, "type")

    def get_kind_of(self, name: str) -> Optional[_SymbolKind]:
        return self.get_symbol_info(name, "kind")

    def get_index_of(self, name: str) -> int:
        return self.get_symbol_info(name, "index")
    
    def get_symbol_info(self, name: str, info_type: str) -> Optional[_SymbolKind | str | int]:
        # symbol is in neither table
        if name not in self.method_symbols and name not in self.class_symbols:
            return None
        
        target_table = self.method_symbols if name in self.method_symbols else self.class_symbols
        symbol = target_table[name]

        if info_type == "type":
            return symbol[0]
        elif info_type == "kind":
            return symbol[1]
        else: # "index"
            return symbol[2]