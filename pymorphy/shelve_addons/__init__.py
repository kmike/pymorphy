#coding: utf8
import shelve
from struct import pack, unpack
import marshal


class ShelfKeyTransform(shelve.DbfilenameShelf):
    ''' Shelf class with key transform hooks.
        You should override key_to_internal and key_to_external methods in subclasses.
    '''
    def key_to_internal(self,key):
        return key
    def key_to_external(self,key):
        return key

    def __init__(self, filename, flag, protocol=None, writeback=False, cached=True):
        ''' use cached=True only for read-only databases!!! '''
        cached = (flag is 'r') and cached

        shelve.DbfilenameShelf.__init__(self, filename, flag, protocol, writeback)
        if cached:
            self.__getitem__ = self._getitem_cached
            self.get = self._get_cached

    def keys(self):
        return [self.key_to_external(key) for key in self.dict.keys()]

    def __contains__(self, key):
        return self.dict.has_key(self.key_to_internal(key))

    def has_key(self, key):
        return self.dict.has_key(self.key_to_internal(key))

    def get(self, key, default=None):
        key_e = self.key_to_internal(key)
        if self.dict.has_key(key_e):
            return self[key_e]
        return default

    def __getitem__(self, key):
        key_e = self.key_to_internal(key)
        return marshal.loads(self.dict[key_e])

    def __setitem__(self, key, value):
        self.dict[self.key_to_internal(key)] = marshal.dumps(value)

    def __delitem__(self, key):
        del self.dict[self.key_to_internal(key)]

    def _get_cached(self, key, default=None):
        if key in self.cache:
            return self.cache[key]
        key_e = self.key_to_internal(key)
        if self.dict.has_key(key_e):
            return self[key_e]
        return default

    def _getitem_cached(self, key):
        if key in self.cache:
            return self.cache[key]
        key_e = self.key_to_internal(key)
        value = marshal.loads(self.dict[key_e])
        self.cache[key]=value
        return value



class ShelfUnicode(ShelfKeyTransform):
    ''' Shelf that accepts unicode keys and encode them to utf8 before passing to lower-level backend.
    '''
    def key_to_external(self,key):
        return unicode(key,'utf8')

    def key_to_internal(self,key):
        return unicode(key).encode('utf8')

class ShelfInteger(ShelfKeyTransform):
    ''' Shelf that accepts integer (0<=key<=65535) keys and encode them to byte strings
        before passing to lower-level backend.
    '''

    def key_to_external(self, key):
        return unpack('H', str)

    def key_to_internal(self, key):
        return pack("H", key)

#from pytc_shelve import shelve_open_int, shelve_open_unicode
#from cdb_shelve import shelve_open_int, shelve_open_unicode

def shelve_open_unicode(filename, flag='c', protocol=None, writeback=False):
    return ShelfUnicode(filename, flag, protocol, writeback)

def shelve_open_int(filename, flag='c', protocol=None, writeback=False):
    return ShelfInteger(filename, flag, protocol, writeback)
