#-*- coding: UTF-8

import re

# Порядок важен: ЯНЦ должно быть перед ЯН для правильного срабатывания
lastname_pattern = re.compile(ur'(.*('
    ur'ОВ|ИВ|ЕВ'
    ur'|ИН'
    ur'|СК|ЦК'
    ur'|ИЧ'
    ur'|ЮК|УК'
    ur'|ИС|ЭС|УС'
    ur'|УНЦ|ЯНЦ|ЕНЦ|АН|ЯН'
    ur'))',
    re.UNICODE | re.VERBOSE)

consonants = u'БВГДЖЗКЛМНПРСТФХЦЧШЩ'

# http://www.gramota.ru/spravka/letters/?rub=rubric_482

# 13.1.1, 13.1.3
cases_ov = {
    u'мр': (u'', u'А', u'У', u'А', u'ЫМ', u'Е'),
    u'жр': (u'А', u'ОЙ', u'ОЙ', u'У', u'ОЙ', u'ОЙ'),
}
# 13.1.2
cases_sk = {
    u'мр': (u'ИЙ', u'ОГО', u'ОМУ', u'ОГО', u'ИМ', u'ОМ'),
    u'жр': (u'АЯ', u'ОЙ', u'ОЙ', u'УЮ', u'ОЙ', u'ОЙ'),
}
cases_ch = {
    u'мр': (u'', u'А', u'У', u'А', u'ЕМ', u'Е'),
    u'жр': (u'', u'', u'', u'', u'', u''),
}
# Фамилии заканчивающиеся на -ок
cases_ok = {
    u'мр': (u'ОК', u'КА', u'КУ', u'КА', u'КОМ', u'КЕ'),
    u'жр': (u'ОК', u'ОК', u'ОК', u'ОК', u'ОК', u'ОК'),
}
# Литовские, эстонские, часть армянских
cases_is = {
    u'мр': (u'', u'А', u'У', u'А', u'ОМ', u'Е'),
    u'жр': (u'', u'', u'', u'', u'', u''),
}
# 13.1.12 (not really)
cases_ia = {
    u'мр': (u'ИЯ', u'ИЮ', u'ИИ', u'ИЮ', u'ИЕЙ', u'ИИ'),
    u'жр': (u'ИЯ', u'ИЮ', u'ИИ', u'ИЮ', u'ИЕЙ', u'ИИ'),
}
# 13.1.6, 13.1.10
indeclinable_cases = {
    u'мр': (u'', u'', u'', u'', u'', u''),
    u'жр': (u'', u'', u'', u'', u'', u''),
}

casemap = {
    u'ОВ': cases_ov,
    u'ИВ': cases_ov,
    u'ЕВ': cases_ov,
    u'ИН': cases_ov,
    u'СК': cases_sk,
    u'ЦК': cases_sk,
    u'ИЧ': cases_ch,
    u'ЮК': cases_ch,
    u'УК': cases_ch,
    u'ИС': cases_is,
    u'ЭС': cases_is,
    u'УС': cases_is,
    # Часть армянских фамилий склоняется так же как литовские
    u'АН': cases_is,
    u'ЯН': cases_is,
    # Другая часть армянских фамилий склоняется как украинские
    # заканчивающиеся на ИЧ
    u'УНЦ': cases_ch,
    u'ЯНЦ': cases_ch,
    u'ЕНЦ': cases_ch,
    u'ИЯ': cases_ia,
    u'ОК': cases_ok,
    u'ЫХ': indeclinable_cases,
    u'ИХ': indeclinable_cases,
    u'КО': indeclinable_cases,
    u'ИА': indeclinable_cases,
    u'ОВО': indeclinable_cases,
    u'АГО': indeclinable_cases,
    u'ЯГО': indeclinable_cases,
}


def decline_lastname_ru(lastname, gender_tag):
    '''Просклонять фамилию и вернуть все возможные формы склонения для заданого
    рода'''

    # Из фамилии выделяется предполагаемая лемма (Табуретов -> Табуретов,
    # Табуретовым -> Табуретов), лемма склоняется по правилам склонения фамилий

    name = lastname_pattern.search(lastname)
    name = (name and name.group(1) or lastname)
    name_len = len(name)

    # Попытка угадать склонённую фамилию из 13.1.12 ("Берией")
    if name_len > 2 and name[-2:] in (u'ИИ', u'ИЮ',):
        name = u'%s%s' % (lastname[:-2], u'ИЯ')
    elif name_len > 3 and name[-3:] in (u'ИЕЙ',):
        name = u'%s%s' % (lastname[:-3], u'ИЯ')

    # Попытка угадать склонённую фамилию закачивающуюся на -ок ("Цапка")
    # Только если буква перед окончанием согласная
    # Проверка согласной делается для исключения склонённых фамилий на -ак
    # ("Собчака")
    if name_len > 3 and name[-2:] in (u'КА', u'КУ', u'КЕ',) \
        and name[-3] in consonants: name = u'%s%s' % (lastname[:-2], u'ОК')
    elif name_len > 4 and name[-3:] in (u'КОМ',) \
        and name[-4] in consonants: name = u'%s%s' % (lastname[:-3], u'ОК')

    cases = {}
    if name_len > 2:
        cases = casemap.get(name[-2:], {})

    if not cases and name_len > 3:
        cases = casemap.get(name[-3:], {})

    # В случае 13.1.12, лемма состоит из фамилии за исключением
    # двух последних букв
    if cases is cases_ia or cases is cases_ok:
        name = name[:-2]

    if not cases:
        return {}

    forms = []
    for i, case in zip(xrange(6), (u'им', u'рд', u'дт', u'вн', u'тв', u'пр',)):
#       print u'%s%s' % (name, cases[gender_tag][i])
        forms.append({
            'word': u'%s%s' % (name, cases[gender_tag][i]),
            'class': u'С',
            'info': u','.join((gender_tag, u'ед', u'фам', case)),
            'lemma': name,
            'method': u'decline_lastname (%s)' % lastname,
            'norm': u'%s%s' % (name, cases[gender_tag][0]),
        })

    return forms


def lastname_normal_form_ru(morph, word, gender_tag):
    ''' Вернуть нормальную форму (единственное число) фамилии для заданого пола
    '''

    # Фамилия склоняется, если в результате склонения получилась исходная форма,
    # возвращается нормальная форма
    for item in decline_lastname_ru(word, gender_tag):
#       print item.get('word'), item.get('info')
        if item.get('word', '') == word:
            return item.get('norm', word)

    # Если в результате склонения исходной формы не получилось,
    # возвращается результат нормализации слова как существительного
    return morph.inflect_ru(word, u'%s,%s,%s' % (u'им', u'ед', gender_tag))
