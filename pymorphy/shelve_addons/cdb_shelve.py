#coding: utf-8

""" Попытка сделать shelve через cdb. Работает сильно медленнее, чем
    bsddb, использовать не стоит.
"""

import cdb
from struct import pack, unpack
from pymorphy.shelve_addons import ShelfKeyTransform
from shelve import Shelf

class CdbWriteDict(object):

    def __init__(self, filename):
        self.db = cdb.cdbmake(filename, filename+'.tmp')

    def __setitem__(self, key, value):
        self.db.add(key, value)

    def close(self):
        return self.db.finish()


class CdbReadDict(object):

    def __init__(self, filename):
        self.db = cdb.init(filename)

    def __getitem__(self, key):
        return self.db[key]

    def has_key(self, key):
        return self.db.has_key(key)


class CdbShelf(ShelfKeyTransform):
    def __init__(self, filename, flag='c', protocol=None, writeback=False):
        if flag=='r':
            self.__getitem__ = self._getitem_cached
            self.get = self._get_cached
            return Shelf.__init__(self, CdbReadDict(filename), protocol, writeback)
        elif flag=='c':
            return Shelf.__init__(self, CdbWriteDict(filename), protocol, writeback)
        else:
            raise NotImplementedError


class ShelfUnicode(CdbShelf):
    ''' Shelf that accepts unicode keys and encode them to utf8 before passing to lower-level backend.
    '''
    def key_to_external(self,key):
        return unicode(key,'utf8')

    def key_to_internal(self,key):
        return unicode(key).encode('utf8')

class ShelfInteger(CdbShelf):
    ''' Shelf that accepts integer (0<=key<=65535) keys and encode them to byte strings
        before passing to lower-level backend.
    '''

    def key_to_external(self, key):
        return unpack('H', str)

    def key_to_internal(self, key):
        return pack("H", key)


def shelve_open_unicode(filename, flag='c', protocol=None, writeback=False):
    return ShelfUnicode(filename, flag, protocol, writeback)

def shelve_open_int(filename, flag='c', protocol=None, writeback=False):
    return ShelfInteger(filename, flag, protocol, writeback)


