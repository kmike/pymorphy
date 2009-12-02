#coding: utf-8

import os

from pymorphy.constants import PRODUCTIVE_CLASSES
from pymorphy.backends import PickledDict, ShelveDict

class Morph:
    def __init__(self, lang, data_source, check_prefixes = True,
                 predict_by_prefix = True, predict_by_suffix = True,
                 handle_EE = False, use_psyco = True):

        self.data = data_source
        self.data.load()

        self.check_prefixes = check_prefixes
        self.predict_by_prefix = predict_by_prefix
        self.predict_by_suffix = predict_by_suffix

        self.prediction_max_prefix_len = 5 #actually 5=4+1
        self.prediction_min_suffix_len = 3 #actually 3=4-1

        self.use_psyco = use_psyco
        if use_psyco:
            try:
                import psyco
                import shelve_addons
                psyco.bind(self._get_lemma_graminfo)
                psyco.bind(shelve_addons.ShelfKeyTransform._getitem_cached)
                psyco.bind(shelve_addons.ShelfKeyTransform.__contains__)
                psyco.bind(self._word_split_variants)
            except ImportError:
                self.use_psyco=False
        self.handle_EE = handle_EE

    def normalize(self, word):
        return set([item['norm'] for item in self._get_graminfo(word)])

    def get_graminfo(self, word):
        return self._get_graminfo(word)

#----------- protected methods -------------

    def _word_split_variants(self,word):
        l = len(word)
        vars = [(word[0:i], word[i:l]) for i in range(1,l)]
        vars.append((word,'',))
        return vars

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

    def _predict_by_suffix(self, word):
        deep = 0
        gram=[]
        for i in (5,4,3,2,1):
            end = word[-i:]
            if end in self.data.endings:
                ending_rules = self.data.endings[end]
                for rule_id in ending_rules:
                    paradigm_ids = ending_rules[rule_id]
                    rule_row = self.data.rules[rule_id]
                    for num in paradigm_ids:
                        rule = rule_row[num]
                        suffix = rule[0]
                        suffix_len = len(suffix)
                        ancode = rule[1]
                        graminfo = self.data.gramtab[ancode]
                        norm_form = word[0:-suffix_len]+rule_row[0][0]
                        if graminfo[0] in PRODUCTIVE_CLASSES:
                            gram.append({'norm': norm_form,'class':graminfo[0],
                                   'info': graminfo[1],
                                   'rule':rule_id, 'ancode': ancode,
                                   'method': 'predict(...%s)' % end
                                   })

    #            print endings[variant[1]]
                if gram:
                    break
#                if forms:
#                    deep+=1
#                if deep==1:
#                    break
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

        variants = self._word_split_variants(word)
        for (prefix, suffix) in variants:
            print prefix, suffix
            if prefix in self.data.lemmas:
                gram.extend([info for info in self._get_lemma_graminfo(prefix, prefix, suffix, require_prefix, 'lemma(%s).suffix(%s)')])

        gram.extend(self._static_prefix_graminfo(variants, require_prefix))

        if not gram and self.handle_EE and predict_EE:
            gram.extend(self._handle_EE(word, require_prefix))

        if not gram and predict and self.predict_by_prefix:
            gram.extend(self._predict_by_prefix_graminfo(word, require_prefix))

        if not gram and predict and self.predict_by_suffix:
            gram.extend(self._predict_by_suffix(word))

        return gram


def get_shelve_morph(lang, check_prefixes = True, predict_by_prefix = True,
                     predict_by_suffix = True, handle_EE = False,
                     use_psyco = True):
    dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', 'dicts','converted',lang))
    data_source = ShelveDict(dir)
    return Morph(lang, data_source, check_prefixes, predict_by_prefix, predict_by_suffix, handle_EE, use_psyco)


def get_pickle_morph(lang, check_prefixes = True, predict_by_prefix = True,
                     predict_by_suffix = True, handle_EE = False, use_psyco = True):
    file = os.path.join(os.path.dirname(__file__),'..','dicts','converted',lang,'morphs.pickle')
    data_source = PickledDict(file)
    return Morph(lang, data_source, check_prefixes, predict_by_prefix, predict_by_suffix, handle_EE, use_psyco)
