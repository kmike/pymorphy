#coding: utf-8
from __future__ import absolute_import

from dicts import morph_ru
from data.basic import BASIC_TESTS

def parse_test_data(test):
    lines = test.splitlines()
    data = {}
    word = None
    for line in lines:
        parts = line.split()
        if len(parts) == 1:
            word = parts[0].upper().replace(u'Ё', u'Е')
            data[word] = []
        elif len(parts) == 2:
            data[word].append({'norm': parts[0], 'class': parts[1], 'info': ''})
        elif len(parts) == 3:
            data[word].append({'norm': parts[0], 'class': parts[1], 'info': parts[2]})
        else:
            print "!!====", line
    for word in data:
        for form in data[word]:
            form['norm'] = form['norm'].upper().replace(u'Ё', u'Е')
    return data

def _normal_form_match(expected_norm, actual_norm):
    variants = [form.strip("()") for form in expected_norm.split('|')]
    return any([norm == actual_norm for norm in variants])

def _gram_info_match(expected_info, actual_info):
    actual_grammems = set([gr for gr in actual_info.split(',') if gr])

    if expected_info.startswith('[') and expected_info.endswith(']'):
        # вся информация опциональна
        expected = expected_info.strip('[]').replace('[,', ',[').split(',')
        must_grammems = set([])
        allowed_grammems = set([gr.strip('[]') for gr in expected])
    else:
        expected = expected_info.replace('[,', ',[').split(',')
        must_grammems = set([gr for gr in expected if not gr.startswith('[')])
        allowed_grammems = set([gr.strip('[]') for gr in expected])

#    print actual_grammems, ' || ', must_grammems, ' | ' , allowed_grammems

    return must_grammems.issubset(actual_grammems) and \
           allowed_grammems.issuperset(actual_grammems)

def forms_match(expected, actual):
    """ Совпадает ли ожидаемый результат разбора с тем, что получился """
    return (expected['class'] == actual['class']) and \
           _normal_form_match(expected['norm'], actual['norm']) and \
           _gram_info_match(expected['info'], actual['info'])


if __name__ == '__main__':

#    print _gram_info_match(u'[imper,1p,pl]', u'1p,pl,imper')
#    exit()

    all = 0
    failed1 = 0
    failed2 = 0

    failed_words = {}

    for test_data in BASIC_TESTS:
        collection = parse_test_data(test_data)
        for word in collection:
            expected_results = collection[word]
            actual_results = morph_ru.get_graminfo(word, True)

            # проверяем, что все стандартные варианты разбора учтены
            for expected_form in expected_results:
                match = any([forms_match(expected_form, actual_form) for actual_form in actual_results])
                if not match:
                    failed1 += 1
                    print ' ----', word, expected_form['class'], expected_form['norm'], expected_form['info']
                    for actual_form in actual_results:
                        print u"   \____ %s %s %s %s" % (word, actual_form['class'], actual_form['norm'], actual_form['info'])
                all += 1

            # проверяем, нет ли у нас лишних (неправильных) вариантов разбора
            for actual_form in actual_results:
                # для каждого варианта разбора смотрим, соответствует ли ему
                # хотя бы 1 разбор в стандарте
                match = any([forms_match(expected_form, actual_form) for expected_form in expected_results])
                if not match:
                    print u" ++++ %s %s %s %s" % (word, actual_form['class'], actual_form['norm'], actual_form['info'])
                    failed2 += 1

    print ' total: %d, failed: %d, extra: %d' % (all, failed1, failed2)
