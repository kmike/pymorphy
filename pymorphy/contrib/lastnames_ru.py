#-*- coding: UTF-8

import itertools
import re

# Порядок важен: ЯНЦ должно быть перед ЯН для правильного срабатывания.
# Несклоняемые фамилии сюда включать необязательно - у них нет леммы
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
# http://planeta-imen.narod.ru/slovar-smolenskich-familij/struktura-familij.html

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
# Белорусские фамилии на -ич, украинские на -ук, -юк
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

# Склонение в множественную форму: общие суффиксы для обоих родов

# Множественная форма для CASES_OV
PLURAL_OV = (u'Ы', u'ЫХ', u'ЫМ', u'ЫХ', u'ЫМИ', u'ЫХ')
# для CASES_SK
PLURAL_SK = (u'ИЕ', u'ИХ', u'ИМ', u'ИХ', u'ИМИ', u'ИХ')
# для CASES_OK
PLURAL_OK = (u'КИ', u'КОВ', u'КАМ', u'КОВ', u'КАМИ', u'КАХ')
# для INDECLINABLE_CASES (и фамилий которые не склоняются во множ. числе)
PLURAL_INDECLINABLE_CASES = (u'', u'', u'', u'', u'', u'')

# Суффикс -> (Склонение единственной формы, Склонение множественной формы)
CASEMAP = {
    u'ОВ': (CASES_OV, PLURAL_OV),
    u'ИВ': (CASES_OV, PLURAL_OV),
    u'ЕВ': (CASES_OV, PLURAL_OV),
    u'ИН': (CASES_OV, PLURAL_OV),
    u'СК': (CASES_SK, PLURAL_SK),
    u'ЦК': (CASES_SK, PLURAL_SK),
    u'ИЧ': (CASES_CH, PLURAL_INDECLINABLE_CASES),
    u'ЮК': (CASES_CH, PLURAL_INDECLINABLE_CASES),
    u'УК': (CASES_CH, PLURAL_INDECLINABLE_CASES),
    u'ИС': (CASES_IS, PLURAL_INDECLINABLE_CASES),
    u'ЭС': (CASES_IS, PLURAL_INDECLINABLE_CASES),
    u'УС': (CASES_IS, PLURAL_INDECLINABLE_CASES),
    # Часть армянских фамилий склоняется так же как литовские
    u'АН': (CASES_IS, PLURAL_INDECLINABLE_CASES),
    u'ЯН': (CASES_IS, PLURAL_INDECLINABLE_CASES),
    # Другая часть армянских фамилий склоняется как украинские
    # заканчивающиеся на ИЧ
    u'УНЦ': (CASES_CH, PLURAL_INDECLINABLE_CASES),
    u'ЯНЦ': (CASES_CH, PLURAL_INDECLINABLE_CASES),
    u'ЕНЦ': (CASES_CH, PLURAL_INDECLINABLE_CASES),
    u'ИЯ': (CASES_IA, PLURAL_INDECLINABLE_CASES),
    u'ОК': (CASES_OK, PLURAL_OK),
    u'ЫХ': (INDECLINABLE_CASES, PLURAL_INDECLINABLE_CASES),
    u'ИХ': (INDECLINABLE_CASES, PLURAL_INDECLINABLE_CASES),
    u'КО': (INDECLINABLE_CASES, PLURAL_INDECLINABLE_CASES),
    u'ИА': (INDECLINABLE_CASES, PLURAL_INDECLINABLE_CASES),
    u'АГО': (INDECLINABLE_CASES, PLURAL_INDECLINABLE_CASES),
    u'ЯГО': (INDECLINABLE_CASES, PLURAL_INDECLINABLE_CASES),
    # TODO: -ец
    # TODO: -хно
}


def decline(lastname):
    ''' Склоняет фамилию и возвращает все возможные формы '''

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

    cases = plural_cases = {}
    if name_len > 2:
        cases, plural_cases = CASEMAP.get(name[-2:], ({}, ()))

    if not cases and name_len > 3:
        cases, plural_cases = CASEMAP.get(name[-3:], ({}, ()))

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

        forms.append({
            'word': u'%s%s' % (name, plural_cases[i]),
            'class': u'С',
            'info': u','.join((u'мр-жр', u'мн', u'фам', case)),
            'lemma': name,
            'method': u'decline_lastname (%s)' % lastname,
            'norm': u'%s%s' % (name, plural_cases[0]),
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
    * gram_form - желаемые характеристики грам. формы (если 'жр' отсутствует в этом параметре, то по-умолчанию принимается 'мр', или 'мр-жр' если указано 'мн')
    '''

    expected_tokens = [token.strip() for token in gram_form.split(',')]

    gender_tag = (u'жр' in expected_tokens and u'жр' or None)
    if not gender_tag:
        gender_tag = (u'мр' in expected_tokens and u'мр' or None)
    if not gender_tag and u'мн' in expected_tokens:
        gender_tag = u'мр-жр'

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

        if item.get('word', '') == lastname:
            # В случае склонения во множественную форму, род игнорируется
            # Род всех (?) фамилий во множественном числе - мр-жр
            if u'мн' in expected_tokens or gender_tag in form_tokens:
                present_in_decline = True

        expected_form = True
        for token in expected_tokens:
            if token not in form_tokens or gender_tag not in form_tokens:
                expected_form = False
                break

        if expected_form:
            accepted = item

    # Если в результате склонения исходной формы не получилось,
    # возвращается результат склонения как для обычного слова

    if present_in_decline and accepted:
        return accepted.get('word', u'')
    else:
        return morph.inflect_ru(lastname, gram_form)


def get_graminfo(lastname):
    '''Вернуть грамматическую информацию о фамилии и её нормальную форму'''

    info = []
    for item in decline(lastname):
        if item.get('word', '') == lastname:
            info.append(item)

    return info


def pluralize(morph, lastname, gram_form=u''):
    '''
    Вернуть фамилию  во множественном числе.

    Параметры:

    * morph - объект Morph
    * lastname - фамилия которую хотим склонять
    * gram_form - желаемые характеристики грам. формы
    '''

    expected_tokens = (gram_form and [
        token.strip() for token in gram_form.split(',')] or [])

    # Удалить из желаемой формы признаки рода и числа
    refined_tokens = [token for token in expected_tokens
        if token not in (u'мр', u'жр', u'мр-жр', u'мн', u'ед')]

    # Если дан gram_form - склонить в указанную форму
    if refined_tokens:
        return inflect(
            morph,
            lastname,
            u','.join(itertools.chain(refined_tokens, (u'мн',))))

    # Иначе - найти форму исходной фамилии и склонить в неё же, но во мн. числе
    # Если в желаемой форме был указан род - использовать как подсказку
    gender_tag = u'жр' in expected_tokens and u'жр' or u'мр'

    for item in decline(lastname):
        form_tokens = [token.strip() for token in item.get('info', u'').split(',')]

        # Проверить наличие исходной формы в заданном роде (аналогично inflect())
        if item.get('word', u'') == lastname and gender_tag in form_tokens:
            for case in (u'им', u'рд', u'дт', u'вн', u'тв', u'пр'):
                if case in form_tokens:
                    return inflect(morph, lastname, u'мн,%s' % case)

    # В случае неудачи - просклонять как обычное слово
    return morph.pluralize_ru(lastname, gram_form)


def pluralize_inflected(morph, lastname, gender_tag, num):
    '''
    Вернуть фамилию в форме, которая будет сочетаться с переданным числом. Например: 1 Попугаев, 2 Попугаевых, 5 Попугаевых.

    Параметры:

    * morph - объект Morph
    * lastname - фамилия которую хотим склонять
    * gender_tag - род фамилии ('мр' или 'жр')
    * num - число
    '''

    if num == 1:
        return normalize(morph, lastname, gender_tag)

    return pluralize(morph, lastname, u'мн,рд,%s' % gender_tag)
