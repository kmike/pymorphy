#coding: utf-8
import unittest

from dicts import morph_en, morph_ru
from pymorphy.morph import GramForm

class MorphTestCase(unittest.TestCase):

    def check_norm(self, input, output):
        norm_forms = morph_ru.normalize(input)
        correct_norm_forms = set(output)

        msg = u"[%s] != [%s]" % (u", ".join(norm_forms), u", ".join(correct_norm_forms))
        self.assertEqual(norm_forms, correct_norm_forms, msg)

    def check_norm_en(self, input, output):
        self.assertEqual(morph_en.normalize(input), set(output))

    def assert_plural(self, word, plural, *args, **kwargs):
        morphed_word = morph_ru.pluralize_ru(word, *args, **kwargs)
        self.assertEqual(morphed_word, plural, u"%s != %s" % (morphed_word, plural))

    def assert_inflect(self, word, form, result, *args, **kwargs):
        morphed_word = morph_ru.inflect_ru(word, form, *args, **kwargs)
        self.assertEqual(morphed_word, result, u"%s != %s" % (morphed_word, result))

    def assert_has_info(self, word, norm=None, cls=None, method=None, scan=False, form=None, standard=False, has_info=True):

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


    def assert_standard(self, word, norm, cls=None, form=None, has_info=True, scan=False):
        return self.assert_has_info(word, norm, cls, None, scan, form, True, has_info)


class TestMorph(MorphTestCase):

    def testNormalize(self):
        self.check_norm(u'КОШКА', [u'КОШКА'])
        self.check_norm(u'КОШКЕ', [u'КОШКА'])
        self.check_norm(u'СТАЛИ', [u'СТАЛЬ', u'СТАТЬ'])

        self.check_norm_en('SOLD', ['SELL'])
        self.check_norm_en('COMPUTERS', ['COMPUTER'])

    def testGlobalPrefixNormalize(self):
        self.check_norm(u'ПСЕВДОКОШКА', [u'ПСЕВДОКОШКА'])
        self.check_norm(u'ПСЕВДОКОШКОЙ', [u'ПСЕВДОКОШКА'])

    def testRulePrefixNormalize(self):
        self.check_norm(u'НАИСТАРЕЙШИЙ', [u'СТАРЫЙ'])
        self.check_norm(u'СВЕРХНАИСТАРЕЙШИЙ', [u'СВЕРХСТАРЫЙ'])
        self.check_norm(u'СВЕРХНАИСТАРЕЙШИЙ', [u'СВЕРХСТАРЫЙ'])
        self.check_norm(u'КВАЗИПСЕВДОНАИСТАРЕЙШЕГО', [u'КВАЗИПСЕВДОСТАРЫЙ'])
        self.check_norm(u'НЕБЕСКОНЕЧЕН', [u'НЕБЕСКОНЕЧНЫЙ'])

    def testPrefixPredict(self):
        self.check_norm(u'МЕГАКОТУ', [u'МЕГАКОТ'])
        self.check_norm(u'МЕГАСВЕРХНАИСТАРЕЙШЕМУ', [u'МЕГАСВЕРХСТАРЫЙ'])

    def testEEbug(self):
        self.check_norm(u'КОТЕНОК', [u'КОТЕНОК'])
        self.check_norm(u'ТЯЖЕЛЫЙ', [u'ТЯЖЕЛЫЙ'])
        self.check_norm(u'ЛЕГОК', [u'ЛЕГКИЙ'])
        # fix dict for this? done.
        # should fail if dictionaries are converted using strip_EE=False option

    def testPronouns(self):

        self.check_norm_en(u'SHE', [u'SHE'])
        self.check_norm_en(u'I', [u'I'])
        self.check_norm_en(u'ME', [u'I'])

        self.check_norm(u'ОНА', [u'ОНА'])
        self.check_norm(u'ЕЙ', [u'ОНА'])
        self.check_norm(u'Я', [u'Я'])
        self.check_norm(u'МНЕ', [u'Я'])
#        self.check_norm(u'ЕГО', [u'ОН', u'ОНО'])
#        self.check_norm(u'ЕМУ', [u'ОН', u'ОНО'])

    def testNoBase(self):
        self.check_norm(u'НАИНЕВЕРОЯТНЕЙШИЙ', [u'ВЕРОЯТНЫЙ'])
        self.check_norm(u'ЛУЧШИЙ', [u'ХОРОШИЙ'])
        self.check_norm(u'НАИЛУЧШИЙ', [u'ХОРОШИЙ'])
        self.check_norm(u'ЧЕЛОВЕК', [u'ЧЕЛОВЕК'])
        self.check_norm(u'ЛЮДИ', [u'ЧЕЛОВЕК'])

    def testPredict(self):
        self.check_norm(u'ТРИЖДЫЧЕРЕЗПИЛЮЛЮОКНАМИ', [u'ТРИЖДЫЧЕРЕЗПИЛЮЛЮОКНА'])
        self.check_norm(u'РАЗКВАКАЛИСЬ',[u'РАЗКВАКАТЬСЯ'])
        self.check_norm(u'КАШИВАРНЕЕ', [u'КАШИВАРНЫЙ'])
        self.check_norm(u'ДЕПЫРТАМЕНТОВ',[u'ДЕПЫРТАМЕНТ'])
        self.check_norm(u'ИЗМОХРАТИЛСЯ',[u'ИЗМОХРАТИТЬСЯ'])

    def testNoProdClassesInPrediction(self):
        self.check_norm(u'БУТЯВКОЙ',[u'БУТЯВКА']) # и никаких местоимений!
        self.check_norm(u'САПАЮТ',[u'САПАТЬ']) # и никаких местоимений!

    def testFemale(self):
        self.check_norm(u'КЛЮЕВУ', [u'КЛЮЕВ'])
        self.check_norm(u'КЛЮЕВА', [u'КЛЮЕВ'])

    def testVerbs(self):
        self.check_norm(u'ГУЛЯЛ', [u'ГУЛЯТЬ'])
        self.check_norm(u'ГУЛЯЛА', [u'ГУЛЯТЬ'])
        self.check_norm(u'ГУЛЯЕТ', [u'ГУЛЯТЬ'])
        self.check_norm(u'ГУЛЯЮТ', [u'ГУЛЯТЬ'])
        self.check_norm(u'ГУЛЯЛИ', [u'ГУЛЯТЬ'])
        self.check_norm(u'ГУЛЯТЬ', [u'ГУЛЯТЬ'])

    def testVerbProducts(self):
        self.check_norm(u'ГУЛЯЮЩИЙ', [u'ГУЛЯТЬ'])
        self.check_norm(u'ГУЛЯВШИ', [u'ГУЛЯТЬ'])
        self.check_norm(u'ГУЛЯЯ', [u'ГУЛЯТЬ'])
        self.check_norm(u'ГУЛЯЮЩАЯ', [u'ГУЛЯТЬ'])
        self.check_norm(u'ЗАГУЛЯВШИЙ', [u'ЗАГУЛЯТЬ'])

    def testDropGender(self):
        self.check_norm(u'КРАСИВЫЙ', [u'КРАСИВЫЙ'])
        self.check_norm(u'КРАСИВАЯ', [u'КРАСИВЫЙ'])
        self.check_norm(u'КРАСИВОМУ', [u'КРАСИВЫЙ'])
        self.check_norm(u'КРАСИВЫЕ', [u'КРАСИВЫЙ'])


class TestGramInfo(unittest.TestCase):

    def testLemmaGramInfo(self):
        info = morph_ru.get_graminfo(u'СУСЛИКАМИ')
        self.assertEqual(len(info), 1)
        info = info[0]
        gram_form = GramForm(info['info'])
        self.assertEqual(gram_form.form, set([u'мр', u'тв', u'мн']))
        self.assertEqual(info['norm'], u'СУСЛИК')
