#coding: utf-8
from __future__ import unicode_literals

NOUNS = ('NOUN', 'С',)
PRONOUNS = ('PN', 'МС',)
PRONOUNS_ADJ = ('PN_ADJ', 'МС-П',)
VERBS = ('Г', 'VERB',  'ИНФИНИТИВ',)
ADJECTIVE = ('ADJECTIVE', 'П',)

PRODUCTIVE_CLASSES = NOUNS + VERBS + ADJECTIVE + ('Н',)

#род
RU_GENDERS_STANDARD = {
    'мр': 'm',
    'жр': 'f',
    'ср': 'n',
    'мр-жр': '', #FIXME: ?
}

# падежи
RU_CASES_STANDARD = {
    'им': 'nom',
    'рд': 'gen',
    'дт': 'dat',
    'вн': 'acc',
    'тв': 'ins',
    'пр': 'loc',
    'зв': 'voc',
}

# числа
RU_NUMBERS_STANDARD = {'ед': 'sg', 'мн': 'pl'}

# лица
RU_PERSONS_STANDARD = {'1л': '1p', '2л': '2p', '3л': '3p'}

# времена
RU_TENSES_STANDARD = {
    'нст': 'pres',
    'прш': 'past',
    'буд': 'pres',          #FIXME: ?
}

# залоги
RU_VOICES_STANDARD = {'дст': 'act', 'стр': 'pass'}

# части речи

RU_CLASSES_STANDARD = {
    'С':              'S',
    'П':              'A',
    'МС':             '-',
    'Г' :             'V',
    'ПРИЧАСТИЕ' :     'V',
    'ДЕЕПРИЧАСТИЕ' :  'V',
    'ИНФИНИТИВ':      'V',
    'МС-ПРЕДК':       '-',
    'МС-П':           '-',
    'ЧИСЛ':           '-',
    'ЧИСЛ-П':         '-',
    'Н':              'ADV',
    'ПРЕДК':          '-',
    'ПРЕДЛ':          'PR',
    'СОЮЗ':           'CONJ',
    'МЕЖД':           'ADV',
    'ЧАСТ':           'ADV',
    'ВВОДН':          'ADV',
    'КР_ПРИЛ':        'A',
    'КР_ПРИЧАСТИЕ':   'V',  #FIXME: ?
    'ПОСЛ':           '-',
    'ФРАЗ':           '-',
}

# старые обозначения
RU_GENDERS = RU_GENDERS_STANDARD.keys()
RU_CASES = RU_CASES_STANDARD.keys()
RU_NUMBERS = RU_NUMBERS_STANDARD.keys()
RU_PERSONS = RU_PERSONS_STANDARD.keys()
RU_TENSES = RU_TENSES_STANDARD.keys()
RU_VOICES = RU_VOICES_STANDARD.keys()

RU_GRAMINFO_STANDARD = dict(list(RU_GENDERS_STANDARD.items()) + list(RU_CASES_STANDARD.items()) +\
                            list(RU_NUMBERS_STANDARD.items()) + list(RU_PERSONS_STANDARD.items()) + \
                            list(RU_TENSES_STANDARD.items()) + list(RU_VOICES_STANDARD.items()))

# данные для упрощения преобразования причастий, деепричастий и инфинитивов в глагол
RU_GRAMINFO_STANDARD.update({'partcp': 'partcp', 'ger': 'ger', 'inf': 'inf'})

# прочие преобразования
RU_GRAMINFO_STANDARD.update({'сравн': 'comp', 'прев': 'supr', 'пвл': 'imper'})

# таблицы нормальных форм для всех частей речи: характерный набор
# грамматическиех атрибутов + часть речи, в которую идет нормализация
# + стандартное представление
#NORMAL_FORMS_RU = {
#    'С':               ('им,ед',          'С',           'S'),
#    'П':               ('им,ед,!прев,!сравн',    'П',    'A'),
#    'МС':              ('им,ед',          'МС',          '-'),
#    'Г' :              ('',               'ИНФИНИТИВ',   'V'),
#    'ПРИЧАСТИЕ' :      ('',               'ИНФИНИТИВ',   'V'),
#    'ДЕЕПРИЧАСТИЕ' :   ('',               'ИНФИНИТИВ',   'V'),
#    'ИНФИНИТИВ':       ('',               'ИНФИНИТИВ',   'V'),
#    'МС-ПРЕДК':        ('',               'МС-ПРЕДК',    '-'),
#    'МС-П':            ('им,ед',          'МС-П',        '-'),
#    'ЧИСЛ':            ('им',             'ЧИСЛ',        '-'),
#    'ЧИСЛ-П':          ('',               'ЧИСЛ-П',      '-'),
#    'Н':               ('',               'Н',           'ADV'),
#    'ПРЕДК':           ('',               'ПРЕДК',       '-'),
#    'ПРЕДЛ':           ('',               'ПРЕДЛ',       'PR'),
#    'СОЮЗ':            ('',               'СОЮЗ',        'CONJ'),
#    'МЕЖД':            ('',               'МЕЖД',        'ADV'),
#    'ЧАСТ':            ('',               'ЧАСТ',        'ADV'),
#    'ВВОДН':           ('',               'ВВОДН',        'ADV'),
#    'КР_ПРИЛ':         ('ед',             'П',            'A'),
#    'КР_ПРИЧАСТИЕ':    ('',               'КР_ПРИЧАСТИЕ','V'),  #FIXME: ?
#    'ПОСЛ':            ('',               'ПОСЛ',        '-'),
#    'ФРАЗ':            ('',               'ФРАЗ',        '-'),
#}
#
## вариант, при котором нормальной формой считается слово в мужском роде
#NORMAL_FORMS_RU_DROP_GENDER = NORMAL_FORMS_RU.copy()
#NORMAL_FORMS_RU_DROP_GENDER.update({
#    'П':               ('им,ед,!прев,!сравн,мр',  'П',    'A'),
#    'КР_ПРИЛ':         ('ед,мр',                  'П',    'A'),
#})

#NORMAL_FORMS_EN = {
#    'ADJECTIVE': ('','ADJECTIVE'),
#    'NUMERAL': ('','NUMERAL'),
#    'ADVERB': ('','ADVERB'),
#    'VERB': ('','VERB'),
#    'MOD': ('','MOD'),
#    'VBE': ('','VBE'),
#    'PN': ('','PN'),
#    'PN_ADJ': ('','PN_ADJ'),
#    'PRON': ('','PRON'),
#    'NOUN': ('','NOUN'),
#    'CONJ': ('','CONJ'),
#    'INT': ('','INT'),
#    'PREP': ('','PREP'),
#    'PART': ('','PART'),
#    'ARTICLE': ('','ARTICLE'),
#    'ORDNUM': ('','ORDNUM'),
#    'POSS': ('','POSS'),
#    '*': ('','*'),
#}
#
#NORMAL_FORMS = {}
#NORMAL_FORMS.update(NORMAL_FORMS_RU)
#NORMAL_FORMS.update(NORMAL_FORMS_EN)
#
#NORMAL_FORMS_DROP_GENDER = NORMAL_FORMS_RU_DROP_GENDER.copy()

#KEEP_GENDER_CLASSES = NOUNS+PRONOUNS+PRONOUNS_ADJ+ADJECTIVE+('КР_ПРИЛ',)