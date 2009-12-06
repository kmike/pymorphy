#coding: utf8
from shelve import DbfilenameShelf
from struct import pack, unpack
import marshal

class ShelfKeyTransform(DbfilenameShelf):
    ''' Shelf class with key transform hooks.
        You should override key_to_internal and key_to_external methods in subclasses.
    '''
    @staticmethod
    def key_to_internal(key):
        return key

    @staticmethod
    def key_to_external(key):
        return key

    def __init__(self, filename, flag, protocol=None, writeback=False, cached=True):
        ''' Use cached=True only for read-only databases. '''
        cached = (flag is 'r') and cached
        DbfilenameShelf.__init__(self, filename, flag, protocol, writeback)
        if cached:
            self.__getitem__ = self._getitem__cached
            self.__contains__ = self._contains__cached


    def __setitem__(self, key, value):
        self.dict[self.key_to_internal(key)] = marshal.dumps(value)


    def __contains__(self, key):
        return self.dict.has_key(self.key_to_internal(key))

    def __getitem__(self, key):
        return marshal.loads(self.dict[self.key_to_internal(key)])

    def _contains__cached(self, key):
        if key in self.cache:
            return True
        return self.dict.has_key(self.key_to_internal(key))

    def _getitem__cached(self, key):
        if key in self.cache:
            return self.cache[key]
        value = marshal.loads(self.dict[self.key_to_internal(key)])
        self.cache[key] = value
        return value


    # а эти методы нам не нужны
    def keys(self):
        raise NotImplementedError
    def has_key(self, key):
        raise NotImplementedError
    def get(self, key, default=None):
        raise NotImplementedError
    def __delitem__(self, key):
        raise NotImplementedError



class ShelfUnicode(ShelfKeyTransform):
    ''' Shelf that accepts unicode keys and encode them to utf8 before passing to lower-level backend.
    '''
    @staticmethod
    def key_to_external(key):
        return unicode(key,'utf8')

    @staticmethod
    def key_to_internal(key):
        return unicode(key).encode('utf8')

class ShelfInteger(ShelfKeyTransform):
    ''' Shelf that accepts integer (0<=key<=65535) keys and encode them to byte strings
        before passing to lower-level backend.
    '''

    @staticmethod
    def key_to_external(key):
        return unpack('H', str)

    @staticmethod
    def key_to_internal(key):
        return pack("H", key)

#from pytc_shelve import shelve_open_int, shelve_open_unicode
#from cdb_shelve import shelve_open_int, shelve_open_unicode

def shelve_open_unicode(filename, flag='c', protocol=None, writeback=False):
    return ShelfUnicode(filename, flag, protocol, writeback)

def shelve_open_int(filename, flag='c', protocol=None, writeback=False):
    return ShelfInteger(filename, flag, protocol, writeback)

