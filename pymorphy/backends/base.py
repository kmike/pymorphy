#coding: utf-8

class DictDataSource(object):
    ''' Absctract base class for dictionary data source.
        Subclasses should make class variables (rules, lemmas, prefixes,
        gramtab, endings, possible_rule_prefixes) accessible through dict
        or list syntax ("duck typing")

        @ivar rules: {paradigm_id->[ (suffix, ancode, prefix) ]}
        @ivar lemmas: {base -> [rule_id]}
        @ivar prefixes: set([prefix])
        @ivar gramtab: {ancode->(type,info,letter)}
        @ivar rule_freq: {paradigm_id->freq}
        @ivar endings: {word_end->{rule_id->(possible_paradigm_ids)}}
        @ivar possible_rule_prefixes: [prefix]
    '''
    def __init__(self):

        # для каждой парадигмы - список правил (приставка, грам. информация,
        # префикс) в формате {paradigm_id->[ (suffix, ancode, prefix) ]}
        self.rules={}

        # для каждой леммы - список номеров парадигм? (способов образования слов),  #TODO: проверить, парадигм ли
        # доступных для данной леммы (основы слова)
        self.lemmas={}

        # набор возможных префиксов и приставок к леммам
        self.prefixes=set()

        # для каждого возможного 5 буквенного окончания - словарь, в котором
        # ключи - номера возможных парадигм, а значения - номера возможных
        # правил
        self.endings = {}

        # грамматическая информация
        self.gramtab={}


        self.possible_rule_prefixes = set()

        # ударения
        self.accents=[]

        # частоты для правил
        self.rule_freq = {}
        self.logs=[]

    def load(self):
        raise NotImplementedError

    def convert_and_save(self, data_obj):
        raise NotImplementedError

    def calculate_rule_freq(self):
        for lemma in self.lemmas:
            for paradigm_id in self.lemmas[lemma]:
                self.rule_freq[paradigm_id] = self.rule_freq.get(paradigm_id,0)+1
