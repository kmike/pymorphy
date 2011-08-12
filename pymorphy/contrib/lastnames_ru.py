#-*- coding: UTF-8
import re

# Порядок важен: ЯНЦ должно быть перед ЯН для правильного срабатывания
LASTNAME_PATTERN = re.compile(ur'(.*('
    ur'ОВ|ИВ|ЕВ'
    ur'|ИН'
    ur'|СК|ЦК'
    ur'|ИЧ'
    ur'|ЮК|УК'
    ur'|ИС|ЭС|УС'
    ur'|УНЦ|ЯНЦ|ЕНЦ|АН|ЯН'
    ur'))',
    re.UNICODE | re.VERBOSE)

# XXX: Й тут нет сознательно?
CONSONANTS = u'БВГДЖЗКЛМНПРСТФХЦЧШЩ'

# http://www.gramota.ru/spravka/letters/?rub=rubric_482

# 13.1.1, 13.1.3
CASES_OV = {
    u'мр': (u'', u'А', u'У', u'А', u'ЫМ', u'Е'),
    u'жр': (u'А', u'ОЙ', u'ОЙ', u'У', u'ОЙ', u'ОЙ'),
}
# 13.1.2
CASES_SK = {
    u'мр': (u'ИЙ', u'ОГО', u'ОМУ', u'ОГО', u'ИМ', u'ОМ'),
    u'жр': (u'АЯ', u'ОЙ', u'ОЙ', u'УЮ', u'ОЙ', u'ОЙ'),
}
CASES_CH = {
    u'мр': (u'', u'А', u'У', u'А', u'ЕМ', u'Е'),
    u'жр': (u'', u'', u'', u'', u'', u''),
}
# Фамилии заканчивающиеся на -ок
CASES_OK = {
    u'мр': (u'ОК', u'КА', u'КУ', u'КА', u'КОМ', u'КЕ'),
    u'жр': (u'ОК', u'ОК', u'ОК', u'ОК', u'ОК', u'ОК'),
}
# Литовские, эстонские, часть армянских
CASES_IS = {
    u'мр': (u'', u'А', u'У', u'А', u'ОМ', u'Е'),
    u'жр': (u'', u'', u'', u'', u'', u''),
}
# 13.1.12 (not really)
CASES_IA = {
    u'мр': (u'ИЯ', u'ИЮ', u'ИИ', u'ИЮ', u'ИЕЙ', u'ИИ'),
    u'жр': (u'ИЯ', u'ИЮ', u'ИИ', u'ИЮ', u'ИЕЙ', u'ИИ'),
}
# 13.1.6, 13.1.10
INDECLINABLE_CASES = {
    u'мр': (u'', u'', u'', u'', u'', u''),
    u'жр': (u'', u'', u'', u'', u'', u''),
}

CASEMAP = {
    u'ОВ': CASES_OV,
    u'ИВ': CASES_OV,
    u'ЕВ': CASES_OV,
    u'ИН': CASES_OV,
    u'СК': CASES_SK,
    u'ЦК': CASES_SK,
    u'ИЧ': CASES_CH,
    u'ЮК': CASES_CH,
    u'УК': CASES_CH,
    u'ИС': CASES_IS,
    u'ЭС': CASES_IS,
    u'УС': CASES_IS,
    # Часть армянских фамилий склоняется так же как литовские
    u'АН': CASES_IS,
    u'ЯН': CASES_IS,
    # Другая часть армянских фамилий склоняется как украинские
    # заканчивающиеся на ИЧ
    u'УНЦ': CASES_CH,
    u'ЯНЦ': CASES_CH,
    u'ЕНЦ': CASES_CH,
    u'ИЯ': CASES_IA,
    u'ОК': CASES_OK,
    u'ЫХ': INDECLINABLE_CASES,
    u'ИХ': INDECLINABLE_CASES,
    u'КО': INDECLINABLE_CASES,
    u'ИА': INDECLINABLE_CASES,
    u'ОВО': INDECLINABLE_CASES,
    u'АГО': INDECLINABLE_CASES,
    u'ЯГО': INDECLINABLE_CASES,
}


def decline(lastname):
    ''' Склоняет фамилию и возвращает все возможные формы для заданного рода '''

    # Из фамилии выделяется предполагаемая лемма (Табуретов -> Табуретов,
    # Табуретовым -> Табуретов), лемма склоняется по правилам склонения фамилий

    name = LASTNAME_PATTERN.search(lastname)
    name = name.group(1) if name else lastname
    name_len = len(name)

    # Попытка угадать склонённую фамилию из 13.1.12 ("Берией")
    if name_len > 2 and name[-2:] in (u'ИИ', u'ИЮ',):
        name = lastname[:-2] + u'ИЯ'
    elif name_len > 3 and name[-3:] in (u'ИЕЙ',):
        name = lastname[:-3] + u'ИЯ'

    # Попытка угадать склонённую фамилию, закачивающуюся на -ок ("Цапка")
    # Работает, только если буква перед окончанием согласная.
    # Проверка согласной делается для исключения склонённых фамилий на -ак
    # ("Собчака")
    if name_len > 3 and name[-2:] in (u'КА', u'КУ', u'КЕ',) and name[-3] in CONSONANTS:
        name = lastname[:-2] + u'ОК'
    elif name_len > 4 and name[-3:] in (u'КОМ',) and name[-4] in CONSONANTS:
        name = lastname[:-3] + u'ОК'

    cases = {}
    if name_len > 2:
        cases = CASEMAP.get(name[-2:], {})

    if not cases and name_len > 3:
        cases = CASEMAP.get(name[-3:], {})

    # В случае 13.1.12 лемма состоит из фамилии, за исключением
    # двух последних букв
    if cases is CASES_IA or cases is CASES_OK:
        name = name[:-2]

    if not cases:
        return {}

    forms = []
    for i, case in zip(xrange(6), (u'им', u'рд', u'дт', u'вн', u'тв', u'пр',)):
        for gender_tag in (u'мр', u'жр',):
            forms.append({
                'word': u'%s%s' % (name, cases[gender_tag][i]),
                'class': u'С',
                'info': u','.join((gender_tag, u'ед', u'фам', case)),
                'lemma': name,
                'method': u'decline_lastname (%s)' % lastname,
                'norm': u'%s%s' % (name, cases[gender_tag][0]),
            })

    return forms


def normalize(morph, lastname, gender_tag):
    '''
    Возвращает нормальную форму (именительный падеж) фамилии для заданного рода
    '''

    # FIXME: эта функция возвращает саму форму, а Morph.normalize возвращает
    # множество (set) возможных форм, одно из двух лучше поправить.

    return inflect(morph, lastname, u'им,ед,%s' % gender_tag)


def inflect(morph, lastname, gram_form):
    '''
    Вернуть вариант фамилии который соотвествует данной грамматической
    форме

    Параметры:

    * morph - объект Morph
    * lastname - фамилия которую хотим склонять
    * gram_form - желаемые характеристики грам. формы (если 'жр' отсутствует в этом параметре, то по-умолчанию принимается 'мр')
    '''

    expected_tokens = [token.strip() for token in gram_form.split(',')]
    gender_tag = (u'жр' in expected_tokens and u'жр' or u'мр')

    # За один проход проверяется, что исходное слово может быть склонено как
    # фамилия и выбирается форма подходящая под gram_form

    present_in_decline = False
    accepted = {}
    for item in decline(lastname):
        form_tokens = [token.strip() for token in item.get('info', '').split(',')]

        # Если в результате склонения не получилось исходной формы - ложное срабатывание

        # Обязательно проверяется род: при склонении в противоположном роде
        # может получиться исходная форма но нас интересует совпадение только в
        # заданном роде

        if item.get('word', '') == lastname and gender_tag in form_tokens:
            present_in_decline = True

        expected_form = True
        for token in expected_tokens:
            if token not in form_tokens:
                expected_form = False
                break

        if expected_form:
            accepted = item

    # Если в результате склонения исходной формы не получилось,
    # возвращается результат склонения как для обычного слова

    if present_in_decline and accepted:
        return accepted.get('word', '')
    else:
        return morph.inflect_ru(lastname, gram_form)


def get_graminfo(lastname):
    '''Вернуть грамматическую информацию о фамилии и её нормальную форму'''

    info = []
    for item in decline(lastname):
        if item.get('word', '') == lastname:
            info.append(item)

    return info