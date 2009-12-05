import pytc

from struct import pack, unpack
from pymorphy.shelve_addons import ShelfKeyTransform
from shelve import Shelf


class PytcShelf(ShelfKeyTransform):
    def __init__(self, filename, flag='c', protocol=None, writeback=False):

        db = pytc.BDB()
        if flag == 'r':
            flags = pytc.BDBOREADER
            self.__getitem__ = self._getitem_cached
            self.get = self._get_cached
        elif flag == 'c':
            flags = pytc.BDBOWRITER | pytc.BDBOREADER | pytc.BDBOCREAT
        else:
            raise NotImplementedError

        db.open(filename, flags)
        return Shelf.__init__(self, db, protocol, writeback)

    def __delitem__(self, key):
        pass

    def __del__(self):
        pass


class ShelfUnicode(PytcShelf):
    ''' Shelf that accepts unicode keys and encode them to utf8 before passing to lower-level backend.
    '''
    def key_to_external(self,key):
        return unicode(key,'utf8')

    def key_to_internal(self,key):
        return unicode(key).encode('utf8')

class ShelfInteger(PytcShelf):
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


