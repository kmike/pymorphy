#coding: utf-8

NOUNS = (u'NOUN', u'С',)
PRONOUNS = (u'PN', u'МС',)
PRONOUNS_ADJ = (u'PN_ADJ', u'МС-П',)
VERBS = (u'Г', u'VERB',  u'ИНФИНИТИВ',)
ADJECTIVE = (u'ADJECTIVE', u'П',)

PRODUCTIVE_CLASSES = NOUNS + VERBS + ADJECTIVE + (u'Н',)

#род
RU_GENDERS_STANDARD = {
    u'мр': 'm',
    u'жр': 'f',
    u'ср': 'n',
    u'мр-жр': '', #FIXME: ?
}

# падежи
RU_CASES_STANDARD = {
    u'им': 'nom',
    u'рд': 'gen',
    u'дт': 'dat',
    u'вн': 'acc',
    u'тв': 'ins',
    u'пр': 'loc',
    u'зв': '',
}

# числа
RU_NUMBERS_STANDARD = {u'ед': 'sg', u'мн': 'pl'}

# лица
RU_PERSONS_STANDARD = {u'1л': '1p', u'2л': '2p', u'3л': '3p'}

# времена
RU_TENSES_STANDARD = {
    u'нст': 'pres',
    u'прш': 'past',
    u'буд': '',          #FIXME: ?
}

# залоги
RU_VOICES_STANDARD = {u'дст': 'act', u'стр': 'pass'}

# части речи

RU_CLASSES_STANDARD = {
    u'С':              'S',
    u'П':              'A',
    u'МС':             '-',
    u'Г' :             'V',
    u'ПРИЧАСТИЕ' :     'V',
    u'ДЕЕПРИЧАСТИЕ' :  'V',
    u'ИНФИНИТИВ':      'V',
    u'МС-ПРЕДК':       '-',
    u'МС-П':           '-',
    u'ЧИСЛ':           '-',
    u'ЧИСЛ-П':         '-',
    u'Н':              'ADV',
    u'ПРЕДК':          '-',
    u'ПРЕДЛ':          'PR',
    u'СОЮЗ':           'CONJ',
    u'МЕЖД':           'ADV',
    u'ЧАСТ':           'ADV',
    u'ВВОДН':          'ADV',
    u'КР_ПРИЛ':        'A',
    u'КР_ПРИЧАСТИЕ':   'V',  #FIXME: ?
    u'ПОСЛ':           '-',
    u'ФРАЗ':           '-',
}

# старые обозначения
RU_GENDERS = RU_GENDERS_STANDARD.keys()
RU_CASES = RU_CASES_STANDARD.keys()
RU_NUMBERS = RU_NUMBERS_STANDARD.keys()
RU_PERSONS = RU_PERSONS_STANDARD.keys()
RU_TENSES = RU_TENSES_STANDARD.keys()
RU_VOICES = RU_VOICES_STANDARD.keys()

RU_GRAMINFO_STANDARD = dict(RU_GENDERS_STANDARD.items() + RU_CASES_STANDARD.items() +\
                            RU_NUMBERS_STANDARD.items() + RU_PERSONS_STANDARD.items() + \
                            RU_TENSES_STANDARD.items() + RU_VOICES_STANDARD.items())

# данные для упрощения преобразования причастий, деепричастий и инфинитивов в глагол
RU_GRAMINFO_STANDARD.update({'partcp': 'partcp', 'ger': 'ger', 'inf': 'inf'})

# прочие преобразования
RU_GRAMINFO_STANDARD.update({'сравн': 'comp', 'прев': 'supr'})

# таблицы нормальных форм для всех частей речи: характерный набор
# грамматическиех атрибутов + часть речи, в которую идет нормализация
# + стандартное представление
#NORMAL_FORMS_RU = {
#    u'С':               (u'им,ед',          u'С',           'S'),
#    u'П':               (u'им,ед,!прев,!сравн',    u'П',    'A'),
#    u'МС':              (u'им,ед',          u'МС',          '-'),
#    u'Г' :              (u'',               u'ИНФИНИТИВ',   'V'),
#    u'ПРИЧАСТИЕ' :      (u'',               u'ИНФИНИТИВ',   'V'),
#    u'ДЕЕПРИЧАСТИЕ' :   (u'',               u'ИНФИНИТИВ',   'V'),
#    u'ИНФИНИТИВ':       (u'',               u'ИНФИНИТИВ',   'V'),
#    u'МС-ПРЕДК':        (u'',               u'МС-ПРЕДК',    '-'),
#    u'МС-П':            (u'им,ед',          u'МС-П',        '-'),
#    u'ЧИСЛ':            (u'им',             u'ЧИСЛ',        '-'),
#    u'ЧИСЛ-П':          (u'',               u'ЧИСЛ-П',      '-'),
#    u'Н':               (u'',               u'Н',           'ADV'),
#    u'ПРЕДК':           (u'',               u'ПРЕДК',       '-'),
#    u'ПРЕДЛ':           (u'',               u'ПРЕДЛ',       'PR'),
#    u'СОЮЗ':            (u'',               u'СОЮЗ',        'CONJ'),
#    u'МЕЖД':            (u'',               u'МЕЖД',        'ADV'),
#    u'ЧАСТ':            (u'',               u'ЧАСТ',        'ADV'),
#    u'ВВОДН':           (u'',               u'ВВОДН',        'ADV'),
#    u'КР_ПРИЛ':         (u'ед',             u'П',            'A'),
#    u'КР_ПРИЧАСТИЕ':    (u'',               u'КР_ПРИЧАСТИЕ','V'),  #FIXME: ?
#    u'ПОСЛ':            (u'',               u'ПОСЛ',        '-'),
#    u'ФРАЗ':            (u'',               u'ФРАЗ',        '-'),
#}
#
## вариант, при котором нормальной формой считается слово в мужском роде
#NORMAL_FORMS_RU_DROP_GENDER = NORMAL_FORMS_RU.copy()
#NORMAL_FORMS_RU_DROP_GENDER.update({
#    u'П':               (u'им,ед,!прев,!сравн,мр',  u'П',    'A'),
#    u'КР_ПРИЛ':         (u'ед,мр',                  u'П',    'A'),
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

#KEEP_GENDER_CLASSES = NOUNS+PRONOUNS+PRONOUNS_ADJ+ADJECTIVE+(u'КР_ПРИЛ',)