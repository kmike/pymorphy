#coding: utf-8

import codecs
from pymorphy.backends.base import DictDataSource
from pymorphy.constants import PRODUCTIVE_CLASSES

class MrdDict(DictDataSource):

    def __init__(self, dict_name, gramtab_name, strip_EE=True):
        super(MrdDict, self).__init__()
        self.dict_name = dict_name
        self.gramtab_name = gramtab_name
        self.strip_EE = strip_EE

    def load(self):
        self._load(self.dict_name, self.gramtab_name)
        self.calculate_rule_freq()
        self._calculate_endings()
        self._cleanup_endings()

#----------- protected methods -------------

    def _section_lines(self, file):
        """ Прочитать все строки в секции mrd-файла, заменяя Ё на Е,
            если установлен параметр strip_EE
        """
        lines_count = int(file.readline())
        for i in xrange(0, lines_count):
            if self.strip_EE:
                yield file.readline().replace(u'Ё',u'Е')
            else:
                yield file.readline()

    def _pass_lines(self, file):
        """ Пропустить секцию """
        for line in self._section_lines(file):
            pass

    def _load_rules(self, file):
        """ Загрузить все парадигмы слов"""
        i=0
        for line in self._section_lines(file):
            line_rules = line.strip().split('%')
            for rule in line_rules:
                if not rule:
                    continue
                #parts: suffix, ancode, prefix
                parts = rule.split('*')
                if len(parts)==2:
                    parts.append('')

                (suffix, ancode, prefix) = parts
                if i not in self.rules:
                    self.rules[i]=[]
                self.rules[i].append(tuple(parts))

                if prefix:
                    self.possible_rule_prefixes.add(prefix)
            i=i+1

    def _load_lemmas(self, file):
        for line in self._section_lines(file):
            record = line.split()
            base, rule_id = record[0], record[1]
            if base not in self.lemmas:
                self.lemmas[base] = []

            self.rule_freq[rule_id] = self.rule_freq.get(rule_id,0)+1

            self.lemmas[base].append(int(rule_id))

    def _load_accents(self, file):
        return self._pass_lines(file)

    def _load_logs(self, file):
        for line in self._section_lines(file):
            self.logs.append(line.strip())

    def _load_prefixes(self, file):
        for line in self._section_lines(file):
            self.prefixes.add(line.strip())

    def _load_gramtab(self, file):
        for line in file:
            line=line.strip()
            if line.startswith('//') or line == '':
                continue
            g = line.split()
            if len(g)==3:
                g.append('')
            ancode, letter, type, info = g[0:4]
            self.gramtab[ancode] = (type, info, letter,)

    def _load(self, filename, gramfile):
        dict_file = codecs.open(filename, 'r', 'utf8')
        self._load_rules(dict_file)
        self._load_accents(dict_file)
        self._load_logs(dict_file)
        self._load_prefixes(dict_file)
        self._load_lemmas(dict_file)
        dict_file.close()

        gram_file = codecs.open(gramfile, 'r', 'utf8')
        self._load_gramtab(gram_file)
        gram_file.close()

    def _calculate_endings(self):
        for lemma in self.lemmas:
            for rule_id in self.lemmas[lemma]:
                rule_row = self.rules[rule_id]
                for index, rule in enumerate(rule_row):
                    rule_suffix, rule_ancode, rule_prefix = rule
                    word = ''.join((rule_prefix,lemma, rule_suffix))
                    for i in range(1,6):  #1,2,3,4,5
                        word_end = word[-i:]
                        if word_end:
                            if word_end not in self.endings:
                                self.endings[word_end] = {}
                            if rule_id not in self.endings[word_end]:
                                self.endings[word_end][rule_id]=set()
                            self.endings[word_end][rule_id].add(index)

    def _cleanup_endings(self):
        for end in self.endings:
            rules = self.endings[end]
            new_rules = {}
            best_rules = {}
            for rule_id in rules:
                rule_row = self.rules[rule_id]
                base_ancode = rule_row[0][1]
                base_gram = self.gramtab[base_ancode]
                word_class = base_gram[0]
                if word_class in PRODUCTIVE_CLASSES:
                    if word_class not in best_rules:
                        best_rules[word_class]=rule_id
                    else:
                        new_freq = self.rule_freq[rule_id]
                        old_freq = self.rule_freq[best_rules[word_class]]
                        if new_freq > old_freq:
                            best_rules[word_class]=rule_id
            for wc in best_rules:
                rule_id = best_rules[wc]
                new_rules[rule_id] = tuple(rules[rule_id])
            self.endings[end] = new_rules
