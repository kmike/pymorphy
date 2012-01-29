#coding: utf-8
from __future__ import print_function
from pymorphy.utils import pprint, get_split_variants


class DictDataSource(object):
    '''
    Absctract base class for dictionary data source.
    Subclasses should make class variables (rules, lemmas, prefixes,
    gramtab, endings, possible_rule_prefixes) accessible through dict
    or list syntax ("duck typing")

    Абстрактный базовый класс для источников данных pymorphy.
    У подклассов должны быть свойства rules, lemmas, prefixes,
    gramtab, endings, possible_rule_prefixes, к которым можно было бы
    обращаться как к словарям, спискам или множествам.

    .. glossary::

        rules
            для каждой парадигмы - список правил (приставка, грам. информация,
            префикс)::

                {paradigm_id->[ (suffix, ancode, prefix) ]}

        lemmas
            для каждой леммы - список номеров парадигм (способов
            образования слов), доступных для данной леммы (основы слова)::

                {base -> [paradigm_id]}

        prefixes
            фиксированые префиксы::

                set([prefix])

        gramtab
            грамматическая информация: словарь, ключи которого - индексы грам.
            информации (анкоды), значения - кортежи
            (часть речи, информация о грам. форме, какая-то непонятная буква)::

                {ancode->(type,info,letter)}

        rule_freq
            частоты для правил, используется при подготовке словарей::

                {paradigm_id->freq}

        endings
            для каждого возможного 5 буквенного окончания - словарь, в котором
            ключи - номера возможных парадигм, а значения - номера возможных
            правил::

                {word_end->{paradigm_id->(possible_paradigm_ids)}}

        possible_rule_prefixes
            набор всех возможных приставок к леммам::

                [prefix]
    '''
    def __init__(self):
        self.rules={}
        self.lemmas={}
        self.prefixes=set()
        self.endings = {}
        self.gramtab={}
        self.possible_rule_prefixes = set()
        self.rule_freq = {}
        self.accents=[] # ударения, не используется
        self.logs=[] # логи работы с оригинальной программой от aot, не используется

    def load(self):
        """ Загрузить данные """
        raise NotImplementedError

    def convert_and_save(self, data_obj):
        """ Взять данные из data_obj (наследник DataDictSource)
            и сохранить из в специфичном для класса формате.
        """
        raise NotImplementedError

    def calculate_rule_freq(self):
        """
        Подсчитать частоту, с которой встречаются различные правила.
        Требуется для предсказателя, чтобы выбирать наиболее распространенные
        варианты.
        """
        for lemma in self.lemmas:
            for paradigm_id in self.lemmas[lemma]:
                self.rule_freq[paradigm_id] = self.rule_freq.get(paradigm_id, 0)+1

#    @profile
    def analyze(self, word):
        """
        Возвращает (lemma, paradigm_id, rule) со всеми вариантами разбора слова.

        lemma - с какой леммой слово разобрали;
        paradigm_id - номер парадигмы;
        rule - подходящее правило в парадигме.

        Подклассы, использующие специализированные структуры для хранения
        словарей, могут реализовать этот метод эффективнее.
        """

        rules = self.rules
        lemmas = self.lemmas

        # Основная проверка по словарю: разбиваем слово на 2 части,
        # считаем одну из них леммой, другую окончанием, пробуем найти
        # лемму в словаре; если нашли, то пробуем найти вариант разбора
        # с подходящим окончанием.
        for lemma, suffix in get_split_variants(word):
            if lemma in lemmas:
                for paradigm_id in lemmas[lemma]:
                    paradigm = rules[paradigm_id]
                    for rule in paradigm:
                        if rule[0] == suffix:
                            yield lemma, paradigm_id, rule

        # Вариант с пустой леммой (например, ЧЕЛОВЕК - ЛЮДИ).
        # У таких слов в словарях основа записана как "#".
        for paradigm_id in lemmas['#']:
            paradigm = rules[paradigm_id]
            for rule in paradigm:
                if rule[0] == word:
                    yield '', paradigm_id, rule


    def _check_self(self):
        """ Проверить словарь на корректность """
        paradigm_ids = self.rules.keys()

        print('checking paradigms...')
        # правила
        for paradigm_id, paradigm_rules in self.rules.iteritems():
            if not paradigm_rules:
                print ('  no rules for paradigm %d' % paradigm_id)
        print ('%d paradigms were checked' % len(paradigm_ids))

        print ('checking lemmas...')
        # леммы
        for base, paradigms in self.lemmas.iteritems():
            for id in paradigms:
                if id not in paradigm_ids:
                    print ('  invalid paradigm %d for lemma %s' % (id, base))
        print ('%d lemmas were checked' % len(self.lemmas.keys()))

    def _check_other(self, other):
        """ Сравнить свои данные с данными из другого источника, считая
        самого себя непогрешимым.  """

        print ("checking other's paradigms...")
        errors = 0
        for paradigm_id, rules in self.rules.iteritems():
            if paradigm_id not in other.rules:
                print ("  paradigm %d doesn't exist" % paradigm_id)
                errors += 1
                continue

            # приводим все к tuple
            other_rules = [tuple(r) for r in other.rules[paradigm_id]]
            if rules != other_rules:
                print ('  paradigm %s is incorrect:' % paradigm_id)
                pprint(rules)
                print ('!=')
                pprint(other_rules)
                print ('--------------------')
                errors += 1
        if errors:
            print ('%d errors found.' % errors)

        errors = 0
        print ("checking other's lemmas...")
        for base, paradigms in self.lemmas.iteritems():
            if base not in other.lemmas:
                print ("  lemma %s doesn't exist" % base)
                errors += 1
                continue
            other_paradigms = other.lemmas[base]
            if paradigms != other_paradigms:
                print ('  lemma %s is incorrect: %s != %s' % (base, other_paradigms, paradigms))
                errors += 1
        if errors:
            print ('%d errors found.' % errors)

