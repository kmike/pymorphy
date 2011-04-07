#coding: utf-8

import codecs
from pymorphy.backends.base import DictDataSource
from pymorphy.constants import PRODUCTIVE_CLASSES


class MrdDataSource(DictDataSource):
    """ Источник данных для морфологического анализатора pymorphy,
        берущий информацию из оригинальных mrd-файлов (в которых кодировка
        была изменена с 1251 на utf-8). Используется для конвертации
        оригинальных данных в простые для обработки ShelveDict или PickledDict.
    """

    def __init__(self, dict_name, gramtab_name, strip_EE=True):
        super(MrdDataSource, self).__init__()
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

                parts[1] = parts[1][:2]
                (suffix, ancode, prefix) = parts
                if i not in self.rules:
                    self.rules[i]=[]
                self.rules[i].append(tuple(parts))

                if prefix:
                    self.possible_rule_prefixes.add(prefix)
            i += 1

    def _load_lemmas(self, file):
        """ Загрузить текущую секцию как секцию с леммами """
        for line in self._section_lines(file):
            record = line.split()
            base, paradigm_id = record[0], record[1]
            if base not in self.lemmas:
                self.lemmas[base] = []

            self.rule_freq[paradigm_id] = self.rule_freq.get(paradigm_id,0)+1

            self.lemmas[base].append(int(paradigm_id))

    def _load_accents(self, file):
        return self._pass_lines(file)

    def _load_logs(self, file):
        """ Загрузить текущую секцию как секцию с логами (бесполезная штука) """
        for line in self._section_lines(file):
            self.logs.append(line.strip())

    def _load_prefixes(self, file):
        """ Загрузить текущую секцию как секцию с префиксами """
        for line in self._section_lines(file):
            self.prefixes.add(line.strip())

    def _load_gramtab(self, file):
        """ Загрузить грамматическую информацию из файла """
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
        """
        Подсчитать все возможные 5-буквенные окончания слов.
        Перебирает все возможные формы всех слов по словарю, смотрит окончание
        и добавляет его в словарь.
        """

        # перебираем все слова
        for lemma in self.lemmas:

            # берем все возможные парадигмы
            for paradigm_id in self.lemmas[lemma]:
                paradigm = self.rules[paradigm_id]

                # все правила в парадигме
                for index, rule in enumerate(paradigm):
                    rule_suffix, rule_ancode, rule_prefix = rule

                    # формируем слово
                    word = ''.join((rule_prefix, lemma, rule_suffix))

                    # добавляем окончания и номера правил их получения в словарь
                    for i in range(1,6):  #1,2,3,4,5
                        word_end = word[-i:]
                        if word_end:
                            if word_end not in self.endings:
                                self.endings[word_end] = {}
                            if paradigm_id not in self.endings[word_end]:
                                self.endings[word_end][paradigm_id]=set()
                            self.endings[word_end][paradigm_id].add(index)


    def _cleanup_endings(self):
        """
        Очистка правил в словаре возможных окончаний. Правил получается много,
        оставляем только те, которые относятся к продуктивным частям речи +
        для каждого окончания оставляем только по 1 самому популярному правилу
        на каждую часть речи.
        """
        for end in self.endings:
            paradigms = self.endings[end]
            result_paradigms = {}
            best_paradigms = {}
            for paradigm_id in paradigms:
                paradigm = self.rules[paradigm_id]
                base_ancode = paradigm[0][1]
                base_gram = self.gramtab[base_ancode]
                word_class = base_gram[0]
                if word_class in PRODUCTIVE_CLASSES:
                    if word_class not in best_paradigms:
                        best_paradigms[word_class]=paradigm_id
                    else:
                        new_freq = self.rule_freq[paradigm_id]
                        old_freq = self.rule_freq[best_paradigms[word_class]]
                        if new_freq > old_freq:
                            best_paradigms[word_class]=paradigm_id

            for wc in best_paradigms:
                paradigm_id = best_paradigms[wc]
                result_paradigms[paradigm_id] = tuple(paradigms[paradigm_id])
            self.endings[end] = result_paradigms

    @staticmethod
    def setup_psyco():
        """ Оптимизировать узкие места в MrdDataSource с помощью psyco """
        try:
            import psyco
            psyco.bind(MrdDataSource._calculate_endings)
            psyco.bind(MrdDataSource._load_lemmas)
            psyco.bind(MrdDataSource._cleanup_endings)
            psyco.bind(MrdDataSource._section_lines)
            psyco.bind(DictDataSource.calculate_rule_freq)
        except ImportError:
            pass
