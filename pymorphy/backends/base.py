#coding: utf-8

class DictDataSource(object):
    ''' Absctract base class for dictionary data source.
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
                self.rule_freq[paradigm_id] = self.rule_freq.get(paradigm_id,0)+1
