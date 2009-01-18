#coding: utf8

"""
Morphological analyser for Russian and English languages
using converted AOT (http://www.aot.ru/download.php) dictionaries.

Conversion script is included.

@author:  Mikhail Korobov <kmike84@gmail.com>
@license: MIT

Copyright (c) Mikhail Korobov <kmike84@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR
A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

import os

NOUNS = ('NOUN','С',)
PRONOUNS = ('PN','МС',)
PRONOUNS_ADJ = ('PN_ADJ','МС-П',)
VERBS = ('Г','VERB',)
ADJECTIVE = ('ADJECTIVE', 'П',)

PRODUCTIVE_CLASSES = ('С', 'П', 'Г', 'Н', 'ИНФИНИТИВ', 'NOUN','VERB', 'ADJECTIVE',) #for predictor

class DictDataSource(object):
    ''' Absctract base class for dictionary data source.
        Subclasses should make class variables (rules, lemmas, prefixes, gramtab,
        endings, possible_rule_prefixes) accessible through dict and list syntax ("duck typing")

        @ivar rules: {rule_num->[ (suffix, ancode, prefix) ]}
        @ivar lemmas: {base -> [rule_id]}
        @ivar prefixes: set([prefix])
        @ivar gramtab: {ancode->(type,info,letter)}
        @ivar rule_freq: {rule_num->freq}
        @ivar endings: {word_end->{rule_id->(possible_rule_nums)}}
        @ivar possible_rule_prefixes: [prefix]
    '''
    def __init__(self):
        self.rules={}
        self.lemmas={}
        self.prefixes=set()
        self.gramtab={}
        self.endings = {}
        self.possible_rule_prefixes = set()

        self.accents=[]
        self.rule_freq = {}
        self.logs=[]

    def load(self):
        raise NotImplementedError

    def convert_and_save(self, data_obj):
        raise NotImplementedError

    def calculate_rule_freq(self):
        for lemma in self.lemmas:
            for rule_num in self.lemmas[lemma]:
                self.rule_freq[rule_num] = self.rule_freq.get(rule_num,0)+1

class PickledDict(DictDataSource):

    def __init__(self, file):
        self.file = file
        super(PickledDict, self).__init__()

    def load(self):
        try:
            from cPickle import Unpickler
        except ImportError:
            from pickle import Unpickler

        pickle_file = open(self.file,'rb')
        p = Unpickler(pickle_file)
        self.lemmas = p.load()
        self.rules = p.load()
        self.gramtab = p.load()
        self.prefixes = p.load()
        self.possible_rule_prefixes = p.load()
        self.endings = p.load()
        self.rule_freq = p.load or {}

    def convert_and_save(self, data_obj):
        try:
            from cPickle import Pickler
        except ImportError:
            from pickle import Pickler

        pickle_file = open(self.file,'wb')
        p = Pickler(pickle_file, -1)
        p.dump(data_obj.lemmas)
        p.dump(data_obj.rules)
        p.dump(data_obj.gramtab)
        p.dump(data_obj.prefixes)
        p.dump(data_obj.possible_rule_prefixes)
        p.dump(data_obj.endings)
        if data_obj.rule_freq:
            p.dump(data_obj.rule_freq)

class ShelveDict(DictDataSource):
    def __init__(self, path='', protocol=-1):
        self.path = path
        self.protocol = protocol
        super(ShelveDict, self).__init__()

    def load(self):
#        import shelve
        import shelve_addons

        self.lemmas = shelve_addons.open_unicode(os.path.join(self.path,'lemmas.shelve'),'r',self.protocol)
        self.rules = shelve_addons.open_int(os.path.join(self.path,'rules.shelve'),'r',self.protocol)
        self.endings = shelve_addons.open_unicode(os.path.join(self.path,'endings.shelve'), 'r', self.protocol)

        misc = shelve_addons.open_unicode(os.path.join(self.path,'misc.shelve'), 'r', self.protocol)
        self.gramtab = misc['gramtab']
        self.prefixes = misc['prefixes']
        self.possible_rule_prefixes = misc['possible_rule_prefixes']

    def convert_and_save(self, data_obj):
#        import shelve
        import shelve_addons

        lemma_shelve = shelve_addons.open_unicode(os.path.join(self.path,'lemmas.shelve'), 'c', self.protocol)
        rules_shelve = shelve_addons.open_int(os.path.join(self.path,'rules.shelve'), 'c', self.protocol)
        endings_shelve = shelve_addons.open_unicode(os.path.join(self.path,'endings.shelve'), 'c', self.protocol)
        misc_shelve = shelve_addons.open_unicode(os.path.join(self.path,'misc.shelve'), 'c', self.protocol)

        for lemma in data_obj.lemmas:
            lemma_shelve[lemma] = data_obj.lemmas[lemma]

        for rule in data_obj.rules:
            rules_shelve[rule] = data_obj.rules[rule]

        for end in data_obj.endings:
            endings_shelve[end] = data_obj.endings[end]

        misc_shelve['prefixes'] = data_obj.prefixes
        misc_shelve['gramtab'] = data_obj.gramtab
        misc_shelve['possible_rule_prefixes'] = data_obj.possible_rule_prefixes

        del misc_shelve

        if data_obj.rule_freq:
            freq_shelve = shelve_addons.open_int(os.path.join(self.path,'freq.shelve'), 'c', self.protocol)
            for (rule, freq,) in data_obj.rule_freq.items():
                freq_shelve[int(rule)] = freq

class MrdDict(DictDataSource):

    def __init__(self, dict_name, gramtab_name, strip_EE=True):
        super(MrdDict, self).__init__()
        self.dict_name = dict_name
        self.gramtab_name = gramtab_name
        self.strip_EE = strip_EE

    def load(self):
        self._load(self.dict_name, self.gramtab_name)
        self.calculate_rule_freq()
        self._calculate_endings()
        self._cleanup_endings()

#----------- protected methods -------------

    def _section_lines(self, file):
        lines_count = int(file.readline())
        for i in xrange(0, lines_count):
            if self.strip_EE:
                yield file.readline().replace(u'Ё',u'Е')
            else:
                yield file.readline()

    def _pass_lines(self, file):
        for line in self._section_lines(file):
            pass

    def _load_rules(self, file):
        i=0
        for line in self._section_lines(file):
            line_rules = line.strip().split('%')
            for rule in line_rules:
                if not rule:
                    continue
                #parts: suffix, ancode, prefix
                parts = rule.split('*')
                if len(parts)==2:
                    parts.append('')

                (suffix, ancode, prefix) = parts
                if i not in self.rules:
                    self.rules[i]=[]
                self.rules[i].append(tuple(parts))

                if prefix:
                    self.possible_rule_prefixes.add(prefix)
            i=i+1

    def _load_lemmas(self, file):
        for line in self._section_lines(file):
            record = line.split()
            base, rule_id = record[0], record[1]
            if base not in self.lemmas:
                self.lemmas[base] = []

            self.rule_freq[rule_id] = self.rule_freq.get(rule_id,0)+1

            self.lemmas[base].append(int(rule_id))

    def _load_accents(self, file):
        return self._pass_lines(file)

    def _load_logs(self, file):
        for line in self._section_lines(file):
            self.logs.append(line.strip())

    def _load_prefixes(self, file):
        for line in self._section_lines(file):
            self.prefixes.add(line.strip())

    def _load_gramtab(self, file):
        for line in file:
            line=line.strip()
            if line.startswith('//') or line == '':
                continue
            g = line.split()
            if len(g)==3:
                g.append('')
            ancode, letter, type, info = g[0:4]
            self.gramtab[ancode] = (type, info, letter,)

    def _load(self, filename, gramfile):
        import codecs
        dict_file = codecs.open(filename, 'r', 'utf8')
        self._load_rules(dict_file)
        self._load_accents(dict_file)
        self._load_logs(dict_file)
        self._load_prefixes(dict_file)
        self._load_lemmas(dict_file)
        dict_file.close()

        gram_file = codecs.open(gramfile, 'r', 'utf8')
        self._load_gramtab(gram_file)
        gram_file.close()

    def _calculate_endings(self):
        for lemma in self.lemmas:
            for rule_id in self.lemmas[lemma]:
                rule_row = self.rules[rule_id]
                for index, rule in enumerate(rule_row):
                    rule_suffix, rule_ancode, rule_prefix = rule
                    word = ''.join((rule_prefix,lemma, rule_suffix))
                    for i in range(1,6):  #1,2,3,4,5
                        word_end = word[-i:]
                        if word_end:
                            if word_end not in self.endings:
                                self.endings[word_end] = {}
                            if rule_id not in self.endings[word_end]:
                                self.endings[word_end][rule_id]=set()
                            self.endings[word_end][rule_id].add(index)

    def _cleanup_endings(self):
        for end in self.endings:
            rules = self.endings[end]
            new_rules = {}
            best_rules = {}
            for rule_id in rules:
                rule_row = self.rules[rule_id]
                base_ancode = rule_row[0][1]
                base_gram = self.gramtab[base_ancode]
                word_class = base_gram[0]
                if word_class in PRODUCTIVE_CLASSES:
                    if word_class not in best_rules:
                        best_rules[word_class]=rule_id
                    else:
                        new_freq = self.rule_freq[rule_id]
                        old_freq = self.rule_freq[best_rules[word_class]]
                        if new_freq > old_freq:
                            best_rules[word_class]=rule_id
            for wc in best_rules:
                rule_id = best_rules[wc]
                new_rules[rule_id] = tuple(rules[rule_id])
            self.endings[end] = new_rules

class Morph:
    def __init__(self, lang, data_source, check_prefixes = True, predict_by_prefix = True,
                 predict_by_suffix = True, handle_EE = False, use_psyco = True):

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
                    rule_nums = ending_rules[rule_id]
                    rule_row = self.data.rules[rule_id]
                    for num in rule_nums:
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
        for rule_num in lemma_rules:
            rules_row = self.data.rules[rule_num]
            for rule in rules_row: #rule : suffix, ancode, prefix
                rule_suffix, rule_ancode, rule_prefix = rule
#                print rule_suffix, rule_ancode, rule_prefix, '-', word_prefix, '-', rule_match
                if rule_suffix==rule_match and rule_prefix==require_prefix:
                    graminfo = self.data.gramtab[rule_ancode]
                    norm_form = word_base+rules_row[0][0]
                    gram.append(
                     {'norm': norm_form,'class':graminfo[0],
                           'info': graminfo[1],
                           'rule':rule_num, 'ancode': rule_ancode,
                           'method': method_format_str % (word_base, rule_match)})
        return gram

    def _flexion_graminfo(self, word, require_prefix):
        return [info for info in self._get_lemma_graminfo('#', '', word, require_prefix, '%snobase(%s)')]

    def _get_graminfo(self, word, require_prefix='', predict = True, predict_EE = True):
        gram = []

        gram.extend(self._flexion_graminfo(word, require_prefix))

        variants = self._word_split_variants(word)
        for (prefix, suffix) in variants:
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
                     predict_by_suffix = True, handle_EE = False, use_psyco = True):
    dir = os.path.join(os.path.dirname(__file__),'dicts','converted',lang)
    data_source = ShelveDict(dir)
    return Morph(lang, data_source, check_prefixes, predict_by_prefix, predict_by_suffix, handle_EE, use_psyco)

def get_pickle_morph(lang, check_prefixes = True, predict_by_prefix = True,
                     predict_by_suffix = True, handle_EE = False, use_psyco = True):
    file = os.path.join(os.path.dirname(__file__),'dicts','converted',lang,'morphs.pickle')
    data_source = PickledDict(file)
    return Morph(lang, data_source, check_prefixes, predict_by_prefix, predict_by_suffix, handle_EE, use_psyco)

if __name__ == '__main__':

    m = get_shelve_morph('ru')
    for form in m.get_graminfo(u'ХАБРАХАБРА'):
        for v in form:
            print v, form[v]
        print '----'