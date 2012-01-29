#coding: utf-8
try:
    from cPickle import Pickler, Unpickler
except ImportError:
    from pickle import Pickler, Unpickler

from pymorphy.backends.base import DictDataSource

class PickleDataSource(DictDataSource):
    """
    Источник данных для морфологического анализатора pymorphy,
    берущий информацию из файлов, куда с помощью pickle были
    сохранены данные. Самый быстрый, но ест уйму памяти (> 100 MB).
    """

    def __init__(self, file):
        self.file = file
        super(PickleDataSource, self).__init__()

    def load(self):
        with open(self.file,'rb') as pickle_file:
            p = Unpickler(pickle_file)
            self.lemmas = p.load()
            self.rules = p.load()
            self.gramtab = p.load()
            self.prefixes = p.load()
            self.possible_rule_prefixes = p.load()
            self.endings = p.load()
            self.rule_freq = p.load or {}

    def convert_and_save(self, data_obj):
        with open(self.file,'wb') as pickle_file:
            p = Pickler(pickle_file, -1)
            p.dump(data_obj.lemmas)
            p.dump(data_obj.rules)
            p.dump(data_obj.gramtab)
            p.dump(data_obj.prefixes)
            p.dump(data_obj.possible_rule_prefixes)
            p.dump(data_obj.endings)
            if data_obj.rule_freq:
                p.dump(data_obj.rule_freq)

    def __str__(self):
        return 'PickleDataSource (%s)' % self.file