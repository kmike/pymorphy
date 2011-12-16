#coding: utf-8
from cdblib import CDB, CDBWriter
from shelf_with_hooks import ShelfWithHooks
from shelve import Shelf

class CDBReader(CDB):
    def has_key(self, key):
        return self.__contains__(key)


class CdblibShelf(ShelfWithHooks):

    def __init__(self, filename, flag, key_type='str', dump_method=None,
                 cached=True, writeback=False):
        if flag=='r':
            Shelf.__init__(self, CDBReader(filename), -1, writeback)
        elif flag=='c':
            Shelf.__init__(self, CDBWriter(filename), -1, writeback)
        self._setup_methods(cached, key_type, dump_method)

    def close(self):
        self.dict.close()
