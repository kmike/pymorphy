#coding: utf8
from shelve import DbfilenameShelf
from struct import pack, unpack
import marshal
import simplejson

class ShelfWithHooks(DbfilenameShelf):
    ''' Shelf class with key and value transform hooks. '''

    DUMP_METHODS = {
        'marshal': {
           'loads': marshal.loads,
           'dumps': marshal.dumps
        },
        'json':  {
           'loads': simplejson.loads,
           'dumps': simplejson.dumps
        },
    }

    KEY_TRANSFORM_METHODS = {
         'unicode': {
             'encode': lambda key: unicode(key).encode('utf8'),
             'decode': lambda key: unicode(key, 'utf8'),
          },
         'int': {
             'encode': lambda key: pack("H", key),
             'decode': lambda key: unpack('H', key),
          },
          'str': {
             'encode': lambda key: key,
             'decode': lambda key: key,
          }
    }

    def __init__(self, filename, flag, key_type='str', dump_method='marshal',
                 cached=True, writeback=False):

        DbfilenameShelf.__init__(self, filename, flag, -1, writeback)
        cached = (flag is 'r') and cached
        self._setup_methods(cached, key_type, dump_method)


    def _setup_methods(self, cached, key_type, dump_method):
        if cached:
            self.__getitem__ = self._getitem__cached
            self.__contains__ = self._contains__cached

        self._encode_key = self.KEY_TRANSFORM_METHODS[key_type]['encode']
        self._decode_key = self.KEY_TRANSFORM_METHODS[key_type]['decode']

        self._dumps_value = self.DUMP_METHODS[dump_method]['dumps']
        self._loads_value = self.DUMP_METHODS[dump_method]['loads']


    def __setitem__(self, key, value):
        self.dict[self._encode_key(key)] = self._dumps_value(value)

    def __contains__(self, key):
        return self.dict.has_key(self._encode_key(key))

    def __getitem__(self, key):
        return self._loads_value(self.dict[self._encode_key(key)])

    def _contains__cached(self, key):
        if key in self.cache:
            return True
        return self.dict.has_key(self._encode_key(key))

    def _getitem__cached(self, key):
        if key in self.cache:
            return self.cache[key]
        value = self._loads_value(self.dict[self._encode_key(key)])
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

    def close(self):
        pass

