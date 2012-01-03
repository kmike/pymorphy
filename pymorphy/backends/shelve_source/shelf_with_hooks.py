#coding: utf8
from shelve import DbfilenameShelf
from struct import pack, unpack
import marshal
try:
    import simplejson as json
except ImportError:
    import json

from pymorphy.py3k import text_type, binary_type

def _to_utf8(s):
    if isinstance(s, binary_type):
        return s
    return s.encode('utf8')


def json_dumps(value):
    return json.dumps(value, ensure_ascii=False).encode('utf8')

class ShelfWithHooks(DbfilenameShelf):
    ''' Shelf class with key and value transform hooks. '''

    DUMP_METHODS = {
        'marshal': {
           'loads': marshal.loads,
           'dumps': marshal.dumps
        },
        'json':  {
           'loads': json.loads,
           'dumps': json_dumps
        },
    }

    KEY_TRANSFORM_METHODS = {
        'unicode': {
             'encode': lambda key: text_type(key),#.encode('utf8'),
             'decode': lambda key: text_type(key),#, 'utf8'),
        },
        'int': {
             'encode': lambda key: pack("H", int(key)),
             'decode': lambda key: unpack('H', key),
        },
        'str': {
             'encode': _to_utf8,
             'decode': lambda key: key,
        }
    }

    DEFAULT_DUMP_METHOD = 'json'

    def __init__(self, filename, flag, key_type='str', dump_method=None,
                 cached=True, writeback=False):
        DbfilenameShelf.__init__(self, filename, flag, -1, writeback)
        cached = (flag is 'r') and cached
        self._setup_methods(cached, key_type, dump_method)


    def _setup_methods(self, cached, key_type, dump_method=None):
        dump_method = dump_method or self.DEFAULT_DUMP_METHOD

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
        key = self._encode_key(key)
        return self.dict.has_key(key)

    def _getitem__cached(self, key):
        if key in self.cache:
            return self.cache[key]
        value = self._loads_value(self.dict[self._encode_key(key)])
        self.cache[key] = value
        return value

    # а эти методы нам не нужны
    def has_key(self, key):
        raise NotImplementedError
    def keys(self):
        raise NotImplementedError
    def get(self, key, default=None):
        raise NotImplementedError
    def __delitem__(self, key):
        raise NotImplementedError

    def close(self):
        pass

