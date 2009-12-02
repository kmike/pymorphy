#coding: utf-8

import os

from pymorphy.constants import PRODUCTIVE_CLASSES
from pymorphy.backends import PickledDict, ShelveDict

def get_split_variants(word):
    """ Вернуть все варианты разбиения слова на 2 части """
    l = len(word)
    vars = [(word[0:i], word[i:l]) for i in range(1,l)]
    vars.append((word,'',))
    return vars


def predict_by_suffix(word, data_source):
    """ Предсказать грамматическую форму и парадигму неизвестного слова
        по последним 5 буквам.

        self.data.endings - все возможные 5,4,3,2,1-буквенные завершения
        слов.
    """
    gram=[]
    for i in (5,4,3,2,1):
        end = word[-i:]
        if end in data_source.endings:

            # парадигмы, по которым могут образовываться слова с таким
            # завершением
            paradigms = data_source.endings[end]

            for paradigm_id in paradigms:

                # номера возможных правил
                rules_id_list = paradigms[paradigm_id]
                # lookup-словарь для правил
                rules_list = data_source.rules[paradigm_id]

                # для всех правил определяем часть речи, если она
                # продуктивная, то добавляем вариант слова
                for id in rules_id_list:
                    rule = rules_list[id]
                    suffix, ancode = rule[0], rule[1]
                    graminfo = data_source.gramtab[ancode]
                    if graminfo[0] in PRODUCTIVE_CLASSES:
                        # норм. форма слова получается заменой суффикса
                        # на суффикс начальной формы
                        norm_form = word[0:-len(suffix)] + rules_list[0][0]
                        gram.append({'norm': norm_form,
                                     'class':graminfo[0],
                                     'info': graminfo[1],
                                     'rule':paradigm_id,
                                     'ancode': ancode,
                                     'method': 'predict(...%s)' % end
                                   })

            # нашли хотя бы одно окончание слова данной длины, больше не ищем
            if gram:
                break
    return gram


class Morph:
    """ Класс, реализующий морфологический анализ на основе словарей из
        data_source
    """

    def __init__(self, lang, data_source, check_prefixes = True,
                 predict_by_prefix = True, predict_by_suffix = True,
                 handle_EE = False):
        '''
        lang: язык, 'ru' или 'en' (еще de можно, если словарь конвертировать)

        data_source: источник данных. Наследник DictDataSource, свойства должны
            поддерживать доступ по ключу.

        check_prefixes: проверять ли вообще префиксы

        predict_by_prefix: предсказывать ли по префиксу

        predict_by_suffix: предсказывать ли по суффиксу

        handle_EE: как обрабатывать букву ё. Если True, то все буквы ё считаются
            равными е, если False - разными буквами. Значение должно совпадать
            с тем, которое указано при конвертации словаря.
        '''

        self.data = data_source
        self.data.load()

        self.check_prefixes = check_prefixes
        self.predict_by_prefix = predict_by_prefix
        self.predict_by_suffix = predict_by_suffix

        self.prediction_max_prefix_len = 5 #actually 5=4+1
        self.prediction_min_suffix_len = 3 #actually 3=4-1

        self.handle_EE = handle_EE

    def normalize(self, word):
        """ Вернуть нормальную форму слова """
        return set([item['norm'] for item in self._get_graminfo(word)])

    def get_graminfo(self, word):
        """ Вернуть грамматическую информацию о слове """
        return self._get_graminfo(word)

    def get_word_form(self, word, form):
        """ Вернуть слово в заданной грамматической форме """
        raise NotImplemented

#----------- protected methods -------------

    def _static_prefix_graminfo(self, variants, require_prefix=''):
        gram = []
        if self.check_prefixes:
            for (prefix, suffix) in variants:
                if prefix in self.data.prefixes:
                    base_forms = self._get_graminfo(suffix, require_prefix=require_prefix, predict=False, predict_EE = False)
                    for form in base_forms:
                        form['norm'] = prefix+form['norm']
                        form['method'] = 'prefix(%s).%s' % (prefix, form['method'])
                    gram.extend(base_forms)
                if prefix in self.data.possible_rule_prefixes:
                    gram.extend(self._get_graminfo(suffix, require_prefix=prefix, predict=False, predict_EE = False))
        return gram

    def _predict_by_prefix_graminfo(self, word, require_prefix):
        gram=[]
        if self.predict_by_prefix:
            l = len(word)
            variants = [(word[:i], word[i:]) for i in range(1,1+min(self.prediction_max_prefix_len,
                                                                    l-self.prediction_min_suffix_len))]
            for (prefix, suffix) in variants:
#                print prefix, suffix
                base_forms = self._get_graminfo(suffix, require_prefix=require_prefix, predict=False, predict_EE = False)
                for form in base_forms:
                    form['norm'] = prefix+form['norm']
                    form['method'] = 'predict-prefix(%s).%s' % (prefix, form['method'])
                base_forms = [form for form in base_forms if form['class'] in PRODUCTIVE_CLASSES]
#                print base_forms
                gram.extend(base_forms)
        return gram

    def _handle_EE(self, word, require_prefix):
        gram = self._get_graminfo(word.replace(u'Е', u'Ё'), require_prefix, predict_EE = False)
        for info in gram:
            info['norm'] = info['norm'].replace(u'Ё', u'Е')
            info['method'] = info['method'].replace(u'Ё', u'Е')
        return gram


    def _get_lemma_graminfo(self, lemma, word_base, rule_match, require_prefix, method_format_str):
        lemma_rules = self.data.lemmas[lemma]
        gram = []
        for paradigm_id in lemma_rules:
            rules_row = self.data.rules[paradigm_id]
            for rule in rules_row: #rule : suffix, ancode, prefix
                rule_suffix, rule_ancode, rule_prefix = rule
#                print rule_suffix, rule_ancode, rule_prefix, '-', word_prefix, '-', rule_match
                if rule_suffix==rule_match and rule_prefix==require_prefix:
                    graminfo = self.data.gramtab[rule_ancode]
                    norm_form = word_base+rules_row[0][0]
                    gram.append(
                     {'norm': norm_form,'class':graminfo[0],
                           'info': graminfo[1],
                           'rule':paradigm_id, 'ancode': rule_ancode,
                           'method': method_format_str % (word_base, rule_match)})
        return gram

    def _flexion_graminfo(self, word, require_prefix):
        return [info for info in self._get_lemma_graminfo('#', '', word, require_prefix, '%snobase(%s)')]

    def _get_graminfo(self, word, require_prefix='', predict = True, predict_EE = True):
        gram = []

        gram.extend(self._flexion_graminfo(word, require_prefix))

        variants = get_split_variants(word)
        for (prefix, suffix) in variants:
            if prefix in self.data.lemmas:
                gram.extend([info for info in self._get_lemma_graminfo(prefix, prefix, suffix, require_prefix, 'lemma(%s).suffix(%s)')])

        gram.extend(self._static_prefix_graminfo(variants, require_prefix))

        if not gram and self.handle_EE and predict_EE:
            gram.extend(self._handle_EE(word, require_prefix))

        if not gram and predict and self.predict_by_prefix:
            gram.extend(self._predict_by_prefix_graminfo(word, require_prefix))

        if not gram and predict and self.predict_by_suffix:
            gram.extend(predict_by_suffix(word, self.data))

        return gram


def get_shelve_morph(lang, **kwargs):
    dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       '..', 'dicts','converted', lang))
    return Morph(lang, ShelveDict(dir), **kwargs)


def get_pickle_morph(lang, **kwargs):
    file = os.path.abspath(os.path.join(os.path.dirname(__file__),
                        '..', 'dicts', 'converted', lang, 'morphs.pickle'))
    return Morph(lang, PickledDict(file), **kwargs)


def setup_psyco():
    ''' Попытаться оптимизировать узкие места с помощью psyco '''
    try:
        import psyco
        from pymorphy.shelve_addons import ShelfKeyTransform
        psyco.bind(Morph._get_lemma_graminfo)
        psyco.bind(ShelfKeyTransform._getitem_cached)
        psyco.bind(ShelfKeyTransform.__contains__)
        psyco.bind(get_split_variants)
    except ImportError:
        pass