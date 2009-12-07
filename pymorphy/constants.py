#coding: utf-8

NOUNS = (u'NOUN', u'С',)
PRONOUNS = (u'PN', u'МС',)
PRONOUNS_ADJ = (u'PN_ADJ', u'МС-П',)
VERBS = (u'Г', u'VERB',  u'ИНФИНИТИВ',)
ADJECTIVE = (u'ADJECTIVE', u'П',)

PRODUCTIVE_CLASSES = NOUNS + VERBS + ADJECTIVE + (u'Н',)

RU_CASES = (u'им', u'рд', u'дт', u'вн', u'тв', u'пр', u'зв',)
RU_NUMBERS = (u'ед', u'мн')
RU_GENDERS = (u'мр', u'жр', u'ср', u'мр-жр')
RU_PERSONS = (u'1л', u'2л', u'3л')
RU_TENSES = (u'нст', u'прш', u'буд')
RU_VOICES = (u'дст', u'стр')