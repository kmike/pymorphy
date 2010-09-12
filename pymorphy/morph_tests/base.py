#coding: utf-8
import unittest

from dicts import morph_en, morph_ru
from pymorphy.morph import GramForm

class MorphTestCase(unittest.TestCase):

    def assertEqualRu(self, word1, word2):
        self.assertEqual(word1, word2, (u"%s != %s" % (word1, word2)).encode('utf8'))

    def assertNormal(self, input, output):
        norm_forms = morph_ru.normalize(input)
        correct_norm_forms = set(output)

        msg = u"[%s] != [%s]" % (u", ".join(norm_forms), u", ".join(correct_norm_forms))
        self.assertEqual(norm_forms, correct_norm_forms, msg)

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
            forms = morph_ru.get_graminfo_scan(word, standard=standard)
        else:
            forms = morph_ru.get_graminfo(word, standard=standard)
        self.assertEqual(any([is_correct(frm) for frm in forms]), has_info)

    def assertStandard(self, word, norm, cls=None, form=None, has_info=True, scan=False):
        self.assertHasInfo(word, norm, cls, None, scan, form, True, has_info)


class TestMorph(MorphTestCase):

    def test_normalize(self):
        self.assertNormal(u'КОШКА', [u'КОШКА'])
        self.assertNormal(u'КОШКЕ', [u'КОШКА'])
        self.assertNormal(u'СТАЛИ', [u'СТАЛЬ', u'СТАТЬ'])

        self.assertNormalEn('SOLD', ['SELL'])
        self.assertNormalEn('COMPUTERS', ['COMPUTER'])

    def test_global_prefix_normalize(self):
        self.assertNormal(u'ПСЕВДОКОШКА', [u'ПСЕВДОКОШКА'])
        self.assertNormal(u'ПСЕВДОКОШКОЙ', [u'ПСЕВДОКОШКА'])

    def test_rule_prefix_normalize(self):
        self.assertNormal(u'НАИСТАРЕЙШИЙ', [u'СТАРЫЙ'])
        self.assertNormal(u'СВЕРХНАИСТАРЕЙШИЙ', [u'СВЕРХСТАРЫЙ'])
        self.assertNormal(u'СВЕРХНАИСТАРЕЙШИЙ', [u'СВЕРХСТАРЫЙ'])
        self.assertNormal(u'КВАЗИПСЕВДОНАИСТАРЕЙШЕГО', [u'КВАЗИПСЕВДОСТАРЫЙ'])
        self.assertNormal(u'НЕБЕСКОНЕЧЕН', [u'НЕБЕСКОНЕЧНЫЙ'])

    def test_prefix_predict(self):
        self.assertNormal(u'МЕГАКОТУ', [u'МЕГАКОТ'])
        self.assertNormal(u'МЕГАСВЕРХНАИСТАРЕЙШЕМУ', [u'МЕГАСВЕРХСТАРЫЙ'])

    def test_EE_bug(self):
        self.assertNormal(u'КОТЕНОК', [u'КОТЕНОК'])
        self.assertNormal(u'ТЯЖЕЛЫЙ', [u'ТЯЖЕЛЫЙ'])
        self.assertNormal(u'ЛЕГОК', [u'ЛЕГКИЙ'])
        # fix dict for this? done.
        # should fail if dictionaries are converted using strip_EE=False option

    def test_pronouns(self):

        self.assertNormalEn(u'SHE', [u'SHE'])
        self.assertNormalEn(u'I', [u'I'])
        self.assertNormalEn(u'ME', [u'I'])

        self.assertNormal(u'ОНА', [u'ОНА'])
        self.assertNormal(u'ЕЙ', [u'ОНА'])
        self.assertNormal(u'Я', [u'Я'])
        self.assertNormal(u'МНЕ', [u'Я'])
#        self.assertNormal(u'ЕГО', [u'ОН', u'ОНО'])
#        self.assertNormal(u'ЕМУ', [u'ОН', u'ОНО'])

    def test_no_base(self):
        self.assertNormal(u'НАИНЕВЕРОЯТНЕЙШИЙ', [u'ВЕРОЯТНЫЙ'])
        self.assertNormal(u'ЛУЧШИЙ', [u'ХОРОШИЙ'])
        self.assertNormal(u'НАИЛУЧШИЙ', [u'ХОРОШИЙ'])
        self.assertNormal(u'ЧЕЛОВЕК', [u'ЧЕЛОВЕК'])
        self.assertNormal(u'ЛЮДИ', [u'ЧЕЛОВЕК'])

    def test_predict(self):
        self.assertNormal(u'ТРИЖДЫЧЕРЕЗПИЛЮЛЮОКНАМИ', [u'ТРИЖДЫЧЕРЕЗПИЛЮЛЮОКНА'])
        self.assertNormal(u'РАЗКВАКАЛИСЬ',[u'РАЗКВАКАТЬСЯ'])
        self.assertNormal(u'КАШИВАРНЕЕ', [u'КАШИВАРНЫЙ'])
        self.assertNormal(u'ДЕПЫРТАМЕНТОВ',[u'ДЕПЫРТАМЕНТ'])
        self.assertNormal(u'ИЗМОХРАТИЛСЯ',[u'ИЗМОХРАТИТЬСЯ'])

    def test_no_prod_classes_in_prediction(self):
        self.assertNormal(u'БУТЯВКОЙ',[u'БУТЯВКА']) # и никаких местоимений!
        self.assertNormal(u'САПАЮТ',[u'САПАТЬ']) # и никаких местоимений!

    def test_female(self):
        self.assertNormal(u'КЛЮЕВУ', [u'КЛЮЕВ'])
        self.assertNormal(u'КЛЮЕВА', [u'КЛЮЕВ'])

    def test_verbs(self):
        self.assertNormal(u'ГУЛЯЛ', [u'ГУЛЯТЬ'])
        self.assertNormal(u'ГУЛЯЛА', [u'ГУЛЯТЬ'])
        self.assertNormal(u'ГУЛЯЕТ', [u'ГУЛЯТЬ'])
        self.assertNormal(u'ГУЛЯЮТ', [u'ГУЛЯТЬ'])
        self.assertNormal(u'ГУЛЯЛИ', [u'ГУЛЯТЬ'])
        self.assertNormal(u'ГУЛЯТЬ', [u'ГУЛЯТЬ'])

    def test_verb_products(self):
        self.assertNormal(u'ГУЛЯЮЩИЙ', [u'ГУЛЯТЬ'])
        self.assertNormal(u'ГУЛЯВШИ', [u'ГУЛЯТЬ'])
        self.assertNormal(u'ГУЛЯЯ', [u'ГУЛЯТЬ'])
        self.assertNormal(u'ГУЛЯЮЩАЯ', [u'ГУЛЯТЬ'])
        self.assertNormal(u'ЗАГУЛЯВШИЙ', [u'ЗАГУЛЯТЬ'])

    def test_drop_gender(self):
        self.assertNormal(u'КРАСИВЫЙ', [u'КРАСИВЫЙ'])
        self.assertNormal(u'КРАСИВАЯ', [u'КРАСИВЫЙ'])
        self.assertNormal(u'КРАСИВОМУ', [u'КРАСИВЫЙ'])
        self.assertNormal(u'КРАСИВЫЕ', [u'КРАСИВЫЙ'])


class TestGramInfo(unittest.TestCase):

    def test_lemma_graminfo(self):
        info = morph_ru.get_graminfo(u'СУСЛИКАМИ')
        self.assertEqual(len(info), 1)
        info = info[0]
        gram_form = GramForm(info['info'])
        self.assertEqual(gram_form.form, set([u'мр', u'тв', u'мн']))
        self.assertEqual(info['norm'], u'СУСЛИК')
