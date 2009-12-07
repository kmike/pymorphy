# coding: utf-8
from shelve import Shelf
import pytc
from shelf_with_hooks import ShelfWithHooks


class PytcHashShelf(ShelfWithHooks):

    DB_CLASS = pytc.HDB

    def __init__(self, filename, flag, key_type='str', dump_method='json',
                 cached=True, writeback=False):

        db = self.DB_CLASS()
        if flag == 'r':
            flags = pytc.BDBOREADER
        elif flag == 'c':
            flags = pytc.BDBOWRITER | pytc.BDBOREADER | pytc.BDBOCREAT
        else:
            raise NotImplementedError

        db.open(filename, flags)
        Shelf.__init__(self, db, -1, writeback)
        self._setup_methods(cached, key_type, dump_method)

    def __delitem__(self, key):
        pass

    def __del__(self):
        self.close()

    def close(self):
        self.dict.close()


class PytcBtreeShelf(PytcHashShelf):
    DB_CLASS = pytc.BDB
