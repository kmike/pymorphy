#coding: utf-8
import cdb
from shelf_with_hooks import ShelfWithHooks
from shelve import Shelf

class CdbWriteDict(object):

    def __init__(self, filename):
        self.db = cdb.cdbmake(filename.encode('utf8'), filename+'.tmp')

    def __setitem__(self, key, value):
        self.db.add(key, value)

    def close(self):
        return self.db.finish()


class CdbReadDict(object):

    def __init__(self, filename):
        self.db = cdb.init(filename.encode('utf8'))

    def __getitem__(self, key):
        return self.db[key]

    def has_key(self, key):
        return self.db.has_key(key)

    def close(self):
        pass


class CdbShelf(ShelfWithHooks):

    def __init__(self, filename, flag, key_type='str', dump_method=None,
                 cached=True, writeback=False):
        if flag=='r':
            Shelf.__init__(self, CdbReadDict(filename), -1, writeback)
        elif flag=='c':
            Shelf.__init__(self, CdbWriteDict(filename), -1, writeback)
        self._setup_methods(cached, key_type, dump_method)

    def close(self):
        self.dict.close()
