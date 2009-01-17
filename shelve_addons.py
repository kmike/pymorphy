#coding: utf8
import shelve

try:
    from cPickle import Pickler, Unpickler
except ImportError:
    from pickle import Pickler, Unpickler

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


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
#        if cached is None:
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
        f = StringIO(self.dict[key_e])
        return Unpickler(f).load()

    def __setitem__(self, key, value):
        f = StringIO()
        p = Pickler(f)
        p.dump(value)
        self.dict[self.key_to_internal(key)] = f.getvalue()

    def __delitem__(self, key):
        del self.dict[self.key_to_internal(key)]

    def _get_cached(self, key, default=None):
        key_e = self.key_to_internal(key)
        if key_e in self.cache:
             return self.cache[key_e]
        if self.dict.has_key(key_e):
            return self[key_e]
        return default

    def _getitem_cached(self, key):
        key_e = self.key_to_internal(key)
        if key_e in self.cache:
             return self.cache[key_e]
        f = StringIO(self.dict[key_e])
        value = Unpickler(f).load()
        self.cache[key_e]=value
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

    def key_to_external(self,key):
        return ord(str[0])+ord(str[1])*256

    def key_to_internal(self,key):
        c1 = key % 256
        c2 = (key >> 8) % 256
        return chr(c1) + chr(c2)

def open_unicode(filename, flag='c', protocol=None, writeback=False):
    return ShelfUnicode(filename, flag, protocol, writeback)

def open_int(filename, flag='c', protocol=None, writeback=False):
    return ShelfInteger(filename, flag, protocol, writeback)
