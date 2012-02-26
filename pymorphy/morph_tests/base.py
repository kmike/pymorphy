#coding: utf-8
from __future__ import unicode_literals, absolute_import
try:
    from django.utils import unittest as unittest2
except ImportError:
    try:
        import unittest2
    except ImportError:
        import unittest as unittest2
        assert hasattr(unittest2, 'expectedFailure')

from pymorphy.py3k import PY3

from .dicts import morph_en, morph_ru
from pymorphy.morph import GramForm
from pymorphy.contrib.scan import get_graminfo_scan

class MorphTestCase(unittest2.TestCase):

    def _msg(self, fmt, w1, w2):
        if PY3:
            return None

        # console fix for python 2
        return fmt.encode('utf8') % (w1.encode('utf8'), w2.encode('utf8'))

    def assertEqualRu(self, word1, word2):
        self.assertEqual(word1, word2, self._msg('%s != %s', word1, word2))

    def assertNotEqualRu(self, word1, word2):
        self.assertNotEqual(word1, word2, self._msg('%s == %s', word1, word2))

    def assertNormal(self, input, output):
        norm_forms = morph_ru.normalize(input)
        correct_norm_forms = set(output)

        msg = "[%s] != [%s]" % (", ".join(norm_forms), ", ".join(correct_norm_forms))
        self.assertEqual(norm_forms, correct_norm_forms, msg.encode('utf8'))

    def assertNormalEn(self, input, output):
        self.assertEqual(morph_en.normalize(input), set(output))

    def assertPlural(self, word, plural, *args, **kwargs):
        morphed_word = morph_ru.pluralize_ru(word, *args, **kwargs)
        self.assertEqualRu(morphed_word, plural)

    def assertInflected(self, word, form, result, *args, **kwargs):
        morphed_word = morph_ru.inflect_ru(word, form, *args, **kwargs)
        self.assertEqualRu(morphed_word, result)

    def assertHasInfo(self, word, norm=None, cls=None, method=None, scan=False, form=None, standard=False, has_info=True):

        def is_correct(frm):
            correct = True
            if norm:
                correct = frm['norm'] == norm
            if method:
                correct = correct and (method in frm['method'])
            if cls:
                correct = correct and (frm['class'] == cls)
            if form:
                gram_filter = GramForm(form)
                gram_form = GramForm(frm['info'])
                correct = correct and gram_form.match(gram_filter)
            return correct

        if scan:
            forms = get_graminfo_scan(morph_ru, word, standard=standard)
        else:
            forms = morph_ru.get_graminfo(word, standard=standard)
        self.assertEqual(any([is_correct(frm) for frm in forms]), has_info)

    def assertStandard(self, word, norm, cls=None, form=None, has_info=True, scan=False):
        self.assertHasInfo(word, norm, cls, None, scan, form, True, has_info)


class TestMorph(MorphTestCase):

    def test_normalize(self):
        self.assertNormal('КОШКА', ['КОШКА'])
        self.assertNormal('КОШКЕ', ['КОШКА'])
        self.assertNormal('СТАЛИ', ['СТАЛЬ', 'СТАТЬ'])

        self.assertNormalEn('SOLD', ['SELL'])
        self.assertNormalEn('COMPUTERS', ['COMPUTER'])

    def test_global_prefix_normalize(self):
        self.assertNormal('ПСЕВДОКОШКА', ['ПСЕВДОКОШКА'])
        self.assertNormal('ПСЕВДОКОШКОЙ', ['ПСЕВДОКОШКА'])

    def test_rule_prefix_normalize(self):
        self.assertNormal('НАИСТАРЕЙШИЙ', ['СТАРЫЙ'])
        self.assertNormal('СВЕРХНАИСТАРЕЙШИЙ', ['СВЕРХСТАРЫЙ'])
        self.assertNormal('СВЕРХНАИСТАРЕЙШИЙ', ['СВЕРХСТАРЫЙ'])
        self.assertNormal('КВАЗИПСЕВДОНАИСТАРЕЙШЕГО', ['КВАЗИПСЕВДОСТАРЫЙ'])
        self.assertNormal('НЕБЕСКОНЕЧЕН', ['НЕБЕСКОНЕЧНЫЙ'])

    def test_prefix_predict(self):
        self.assertNormal('МЕГАКОТУ', ['МЕГАКОТ'])
        self.assertNormal('МЕГАСВЕРХНАИСТАРЕЙШЕМУ', ['МЕГАСВЕРХСТАРЫЙ'])

    def test_EE_bug(self):
        self.assertNormal('КОТЕНОК', ['КОТЕНОК'])
        self.assertNormal('ТЯЖЕЛЫЙ', ['ТЯЖЕЛЫЙ'])
        self.assertNormal('ЛЕГОК', ['ЛЕГКИЙ'])
        # fix dict for this? done.
        # should fail if dictionaries are converted using strip_EE=False option

    def test_pronouns(self):

        self.assertNormalEn('SHE', ['SHE'])
        self.assertNormalEn('I', ['I'])
        self.assertNormalEn('ME', ['I'])

        self.assertNormal('ОНА', ['ОНА'])
        self.assertNormal('ЕЙ', ['ОНА'])
        self.assertNormal('Я', ['Я'])
        self.assertNormal('МНЕ', ['Я'])
#        self.assertNormal('ЕГО', ['ОН', 'ОНО'])
#        self.assertNormal('ЕМУ', ['ОН', 'ОНО'])

    def test_no_base(self):
        self.assertNormal('НАИНЕВЕРОЯТНЕЙШИЙ', ['ВЕРОЯТНЫЙ'])
        self.assertNormal('ЛУЧШИЙ', ['ХОРОШИЙ'])
        self.assertNormal('НАИЛУЧШИЙ', ['ХОРОШИЙ'])
        self.assertNormal('ЧЕЛОВЕК', ['ЧЕЛОВЕК'])
        self.assertNormal('ЛЮДИ', ['ЧЕЛОВЕК'])

    def test_predict(self):
        self.assertNormal('ТРИЖДЫЧЕРЕЗПИЛЮЛЮОКНАМИ', ['ТРИЖДЫЧЕРЕЗПИЛЮЛЮОКНА'])
        self.assertNormal('РАЗКВАКАЛИСЬ',['РАЗКВАКАТЬСЯ'])
        self.assertNormal('КАШИВАРНЕЕ', ['КАШИВАРНЫЙ'])
        self.assertNormal('ДЕПЫРТАМЕНТОВ',['ДЕПЫРТАМЕНТ'])
        self.assertNormal('ИЗМОХРАТИЛСЯ',['ИЗМОХРАТИТЬСЯ'])

    def test_no_prod_classes_in_prediction(self):
        self.assertNormal('БУТЯВКОЙ',['БУТЯВКА']) # и никаких местоимений!
        self.assertNormal('САПАЮТ',['САПАТЬ']) # и никаких местоимений!

    def test_female(self):
        self.assertNormal('КЛЮЕВУ', ['КЛЮЕВ'])
        self.assertNormal('КЛЮЕВА', ['КЛЮЕВ'])

    def test_verbs(self):
        self.assertNormal('ГУЛЯЛ', ['ГУЛЯТЬ'])
        self.assertNormal('ГУЛЯЛА', ['ГУЛЯТЬ'])
        self.assertNormal('ГУЛЯЕТ', ['ГУЛЯТЬ'])
        self.assertNormal('ГУЛЯЮТ', ['ГУЛЯТЬ'])
        self.assertNormal('ГУЛЯЛИ', ['ГУЛЯТЬ'])
        self.assertNormal('ГУЛЯТЬ', ['ГУЛЯТЬ'])

    def test_verb_products(self):
        self.assertNormal('ГУЛЯЮЩИЙ', ['ГУЛЯТЬ'])
        self.assertNormal('ГУЛЯВШИ', ['ГУЛЯТЬ'])
        self.assertNormal('ГУЛЯЯ', ['ГУЛЯТЬ'])
        self.assertNormal('ГУЛЯЮЩАЯ', ['ГУЛЯТЬ'])
        self.assertNormal('ЗАГУЛЯВШИЙ', ['ЗАГУЛЯТЬ'])

    def test_drop_gender(self):
        self.assertNormal('КРАСИВЫЙ', ['КРАСИВЫЙ'])
        self.assertNormal('КРАСИВАЯ', ['КРАСИВЫЙ'])
        self.assertNormal('КРАСИВОМУ', ['КРАСИВЫЙ'])
        self.assertNormal('КРАСИВЫЕ', ['КРАСИВЫЙ'])

    def test_encoding_bugs(self):
        self.assertNormal('ДЕЙСТВИЕ', ['ДЕЙСТВИЕ'])


class TestGramInfo(unittest2.TestCase):

    def test_lemma_graminfo(self):
        info = morph_ru.get_graminfo('СУСЛИКАМИ')
        self.assertEqual(len(info), 1)
        info = info[0]
        gram_form = GramForm(info['info'])
        self.assertEqual(gram_form.form, set(['мр', 'тв', 'мн']))
        self.assertEqual(info['norm'], 'СУСЛИК')
