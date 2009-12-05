#coding: utf-8
import os

from pymorphy.backends.base import DictDataSource
from pymorphy.shelve_addons import shelve_open_int, shelve_open_unicode

class ShelveDict(DictDataSource):
    """ Источник данных для морфологического анализатора pymorphy,
        берущий информацию из key-value базы данных, используя интерфейс
        shelve из стандартной библиотеки. Позволяет не держать все данные
        в памяти и в то же время обеспечивает достаточно быструю скорость
        работы.

        Грамматическая информация и префиксы загружаются в память сразу.
    """
    def __init__(self, path='', protocol=-1):
        self.path = path
        self.protocol = protocol
        super(ShelveDict, self).__init__()

    def _path(self, name):
        return os.path.join(self.path, name)

    def load(self):
        self.lemmas = shelve_open_unicode(self._path('lemmas.shelve'),
                                          'r', self.protocol)

        self.rules = shelve_open_int(self._path('rules.shelve'),
                                     'r', self.protocol)

        self.endings = shelve_open_unicode(self._path('endings.shelve'),
                                           'r', self.protocol)

        misc = shelve_open_unicode(self._path('misc.shelve'), 'r', self.protocol)
        self.gramtab = misc['gramtab']
        self.prefixes = misc['prefixes']
        self.possible_rule_prefixes = misc['possible_rule_prefixes']

    def convert_and_save(self, data_obj):
        lemma_shelve = shelve_open_unicode(self._path( 'lemmas.shelve'),
                                           'c', self.protocol)

        rules_shelve = shelve_open_int(self._path('rules.shelve'),
                                       'c', self.protocol)

        endings_shelve = shelve_open_unicode(self._path('endings.shelve'),
                                             'c', self.protocol)

        misc_shelve = shelve_open_unicode(self._path('misc.shelve'),
                                          'c', self.protocol)

        for lemma in data_obj.lemmas:
            lemma_shelve[lemma] = data_obj.lemmas[lemma]

        for rule in data_obj.rules:
            rules_shelve[rule] = data_obj.rules[rule]

        for end in data_obj.endings:
            endings_shelve[end] = data_obj.endings[end]

        misc_shelve['prefixes'] = data_obj.prefixes
        misc_shelve['gramtab'] = data_obj.gramtab
        misc_shelve['possible_rule_prefixes'] = data_obj.possible_rule_prefixes

        del misc_shelve

        if data_obj.rule_freq:
            freq_shelve = shelve_open_int(self._path('freq.shelve'),
                                          'c', self.protocol)

            for (rule, freq,) in data_obj.rule_freq.items():
                freq_shelve[int(rule)] = freq
