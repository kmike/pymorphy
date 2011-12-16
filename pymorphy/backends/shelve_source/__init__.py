#coding: utf-8
from __future__ import absolute_import
import os

from pymorphy.backends.base import DictDataSource
from .shelf_with_hooks import ShelfWithHooks


class ShelveDataSource(DictDataSource):
    """ Источник данных для морфологического анализатора pymorphy,
        берущий информацию из key-value базы данных, используя модифицированный
        интерфейс shelve из стандартной библиотеки. Позволяет не держать все
        данные в памяти и в то же время обеспечивает достаточно быструю скорость
        работы.

        Грамматическая информация и префиксы загружаются в память сразу.
    """

    def __init__(self, path='', db_type=None, cached=True):
        self.path = path
        self.db_type = db_type or 'sqlite'
        self.cached = cached

        super(ShelveDataSource, self).__init__()

    def load(self):
        self.lemmas = self._get_shelf('lemmas', 'r', 'unicode')
        self.rules = self._get_shelf('rules', 'r', 'int')
        self.endings = self._get_shelf('endings', 'r', 'unicode')

        misc = self._get_shelf('misc', 'r', 'unicode')
        self.gramtab = misc['gramtab']

        self.prefixes = set(misc['prefixes'])
        self.possible_rule_prefixes = set(misc['possible_rule_prefixes'])

    def convert_and_save(self, data_obj):
        lemma_shelve = self._get_shelf('lemmas', 'c', 'unicode')
        rules_shelve = self._get_shelf('rules', 'c', 'int')
        endings_shelve = self._get_shelf('endings', 'c', 'unicode')

        for lemma in data_obj.lemmas:
            lemma_shelve[lemma] = data_obj.lemmas[lemma]

        for rule in data_obj.rules:
            rules_shelve[rule] = data_obj.rules[rule]

        for end in data_obj.endings:
            endings_shelve[end] = data_obj.endings[end]

        misc_shelve = self._get_shelf('misc', 'c', 'unicode')
        misc_shelve['gramtab'] = data_obj.gramtab
        misc_shelve['prefixes'] = list(data_obj.prefixes)
        misc_shelve['possible_rule_prefixes'] = list(data_obj.possible_rule_prefixes)

        if data_obj.rule_freq:
            freq_shelve = self._get_shelf('freq', 'c', 'int')
            for (rule, freq,) in data_obj.rule_freq.items():
                freq_shelve[int(rule)] = freq
            freq_shelve.close()

        lemma_shelve.close()
        misc_shelve.close()
        rules_shelve.close()
        endings_shelve.close()


    def _path(self, name):
        ext = self.db_type
        if 'cdb' in self.db_type:
            ext = 'cdb'
        return os.path.join(self.path, name+'.'+ext)

    def _get_shelf_class(self):

        def python_cdb():
            from .cdb_shelve import CdbShelf
            return CdbShelf

        def tinycdb():
            from .tinycdb_shelve import TinycdbShelf
            return TinycdbShelf

        def cdblib():
            from .cdblib_shelve import CdblibShelf
            return CdblibShelf

        if self.db_type == 'cdb':
            try:
                return python_cdb()
            except ImportError:
                try:
                    return tinycdb()
                except ImportError:
                    return cdblib()

        elif self.db_type == 'tinycdb':
            return tinycdb()

        elif self.db_type == 'python-cdb':
            return python_cdb()

        elif self.db_type == 'cdblib':
            return cdblib()

        elif self.db_type == 'tch':
            from .pytc_shelve import PytcHashShelf
            return PytcHashShelf

        elif self.db_type == 'tcb':
            from .pytc_shelve import PytcBtreeShelf
            return PytcBtreeShelf

        elif self.db_type == 'sqlite':
            from .sqlite_shelve import SqliteShelf
            return SqliteShelf

        elif self.db_type == 'shelve':
            return ShelfWithHooks

        raise Exception('Unsupported backend: %s' % self.db_type)

    def _get_shelf(self, filename, *args, **kwargs):
        path = self._path(filename)
        return self._get_shelf_class()(path, cached=self.cached,  *args, **kwargs)

    def _check_self(self):
        raise NotImplementedError()

    def _check_other(self, data_source):
        raise NotImplementedError()
