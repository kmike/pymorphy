#coding: utf-8
from __future__ import absolute_import
import sqlite3
from shelve import Shelf
from .shelf_with_hooks import ShelfWithHooks


class SqliteDict(object):
    "A dictionary that stores its data in a table in sqlite3 database"

    def __init__(self, filename=None, connection=None, table='shelf'):
        if connection is not None:
            self.conn = connection
        else:
            self.conn = sqlite3.connect(filename, check_same_thread = False)
        self.conn.text_factory = str

        self._table = table

        self.MAKE_SHELF = 'CREATE TABLE IF NOT EXISTS %s (key TEXT PRIMARY KEY, value TEXT NOT NULL)' % self._table
        self.GET_ITEM = 'SELECT value FROM %s WHERE key = ?' % self._table
        self.ADD_ITEM = 'REPLACE INTO %s (key, value) VALUES (?,?)' % self._table
        self.CLEAR_ALL = 'DELETE FROM %s;  VACUUM;' % self._table
        self.HAS_ITEM = 'SELECT 1 FROM %s WHERE key = ?' % self._table

        self.conn.execute(self.MAKE_SHELF)
        self.conn.commit()

    def has_key(self, key):
        return self.conn.execute(self.HAS_ITEM, (key,)).fetchone() is not None

    def __contains__(self, key):
        return self.has_key(key)

    def __getitem__(self, key):
        item = self.conn.execute(self.GET_ITEM, (key,)).fetchone()
        if item is None:
            raise KeyError(key)
        return item[0]

    def __setitem__(self, key, value):
        self.conn.execute(self.ADD_ITEM, (key, value)) #sqlite3.Binary(value)))
#        self.conn.commit()

    def clear(self):
        self.conn.executescript(self.CLEAR_ALL)
        self.conn.commit()

    def sync(self):
        if self.conn is not None:
            self.conn.commit()

    def close(self):
        if self.conn is None:
            return

        try:
            self.conn.commit()
            self.conn.close()
            self.conn = None
        except (sqlite3.ProgrammingError, sqlite3.OperationalError):
            pass

    def __del__(self):
        self.close()


class SqliteShelf(ShelfWithHooks):

    def __init__(self, filename=None, flag='', key_type='unicode',
                 dump_method=None, cached=True,
                 connection=None, table='shelf',):
        Shelf.__init__(self, SqliteDict(filename, connection, table))

        # 'int' type packs integer key to 2-byte sequence and
        # sqlite doesn't support binary data without extra efforts
        if key_type == 'int':
            key_type = 'unicode'

        self._setup_methods(cached, key_type, dump_method)

    def close(self):
        self.dict.close()
