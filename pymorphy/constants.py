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

NORMAL_FORMS = {
    u'С':               (u'им,ед',          u'С'),
    u'П':               (u'им,ед,!прев,!сравн',    u'П'),
    u'МС':              (u'им,ед',          u'МС'),
    u'Г' :              (u'',               u'ИНФИНИТИВ'),
    u'ПРИЧАСТИЕ' :      (u'',               u'ИНФИНИТИВ'),
    u'ДЕЕПРИЧАСТИЕ' :   (u'',               u'ИНФИНИТИВ'),
    u'ИНФИНИТИВ':       (u'',               u'ИНФИНИТИВ'),
    u'МС-ПРЕДК':        (u'',               u'МС-ПРЕДК'),
    u'МС-П':            (u'им,ед',          u'МС-П'),
    u'ЧИСЛ':            (u'им',             u'ЧИСЛ'),
    u'ЧИСЛ-П':          (u'',               u'ЧИСЛ-П'),
    u'Н':               (u'',               u'Н'),
    u'ПРЕДК':           (u'',               u'ПРЕДК'),
    u'ПРЕДЛ':           (u'',               u'ПРЕДЛ'),
    u'СОЮЗ':            (u'',               u'СОЮЗ'),
    u'МЕЖД':            (u'',               u'МЕЖД'),
    u'ЧАСТ':            (u'',               u'ЧАСТ'),
    u'ВВОДН':           (u'',               u'ВВОДН'),
    u'КР_ПРИЛ':         (u'ед',             u'П'),
    u'КР_ПРИЧАСТИЕ':    (u'',               u'КР_ПРИЧАСТИЕ'),
}

KEEP_GENDER_CLASSES = NOUNS+PRONOUNS+PRONOUNS_ADJ+ADJECTIVE+(u'КР_ПРИЛ',)