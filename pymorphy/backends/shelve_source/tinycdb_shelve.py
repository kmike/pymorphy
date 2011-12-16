#coding: utf-8
import tinycdb
from shelf_with_hooks import ShelfWithHooks
from shelve import Shelf

class TinycdbShelf(ShelfWithHooks):

    def __init__(self, filename, flag, key_type='str', dump_method=None,
                 cached=True, writeback=False):
        if flag=='r':
            Shelf.__init__(self, tinycdb.read(filename), -1, writeback)
        elif flag=='c':
            Shelf.__init__(self, tinycdb.create(filename), -1, writeback)
        self._setup_methods(cached, key_type, dump_method)

    def close(self):
        self.dict.close()
