#coding: utf-8
import os

from pymorphy.backends.base import DictDataSource
from shelf_with_hooks import ShelfWithHooks


class ShelveDataSource(DictDataSource):
    """ Источник данных для морфологического анализатора pymorphy,
        берущий информацию из key-value базы данных, используя модифицированный
        интерфейс shelve из стандартной библиотеки. Позволяет не держать все
        данные в памяти и в то же время обеспечивает достаточно быструю скорость
        работы.

        Грамматическая информация и префиксы загружаются в память сразу, .
    """

    def __init__(self, path='', shelf_class=None):
        self.path = path
        self.SHELF_CLASS = shelf_class
        super(ShelveDataSource, self).__init__()

    def load(self):
        self.lemmas = self._get_shelf('lemmas.shelve', 'r', 'unicode')
        self.rules = self._get_shelf('rules.shelve', 'r', 'int')
        self.endings = self._get_shelf('endings.shelve', 'r', 'unicode')

        misc = self._get_shelf('misc.shelve', 'r', 'unicode')
        self.gramtab = misc['gramtab']
        self.prefixes = misc['prefixes']
        self.possible_rule_prefixes = misc['possible_rule_prefixes']

    def convert_and_save(self, data_obj):
        lemma_shelve = self._get_shelf('lemmas.shelve', 'c', 'unicode')
        rules_shelve = self._get_shelf('rules.shelve', 'c', 'int')
        endings_shelve = self._get_shelf('endings.shelve', 'c', 'unicode')

        for lemma in data_obj.lemmas:
            lemma_shelve[lemma] = data_obj.lemmas[lemma]

        for rule in data_obj.rules:
            rules_shelve[rule] = data_obj.rules[rule]

        for end in data_obj.endings:
            endings_shelve[end] = data_obj.endings[end]

        misc_shelve = self._get_shelf('misc.shelve', 'c', 'unicode')
        misc_shelve['prefixes'] = data_obj.prefixes
        misc_shelve['gramtab'] = data_obj.gramtab
        misc_shelve['possible_rule_prefixes'] = data_obj.possible_rule_prefixes
        del misc_shelve

        if data_obj.rule_freq:
            freq_shelve = self._get_shelf('freq.shelve', 'c', 'int')
            for (rule, freq,) in data_obj.rule_freq.items():
                freq_shelve[int(rule)] = freq


    def _path(self, name):
        return os.path.join(self.path, name)

    def _get_shelf(self, filename, *args, **kwargs):
        path = self._path(filename)
        if self.SHELF_CLASS is not None:
            return self.SHELF_CLASS(path, *args, **kwargs)

        if filename.endswith('.cdb'):
            from cdb_shelve import CdbShelf
            return CdbShelf(path, *args, **kwargs)
        return ShelfWithHooks(path, *args, **kwargs)
