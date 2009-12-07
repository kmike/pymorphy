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