#coding: utf-8
import unittest

import pymorphy

def repeat(n):
    def repeatn(f):
        def inner(*args, **kwds):
            for i in range(n):
                ret = f(*args, **kwds)
            return ret
        return inner
    return repeatn

class TestMorphShelve(unittest.TestCase):
    morph_ru = pymorphy.get_shelve_morph('ru')
    morph_en = pymorphy.get_shelve_morph('en')

#    @repeat(10)
    def check_norm(self, input, output):
        self.assertEqual(self.morph_ru.normalize(input), set(output))

#    @repeat(10)
    def check_norm_en(self, input, output):
        self.assertEqual(self.morph_en.normalize(input), set(output))

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
        self.check_norm(u'ЕГО', [u'ОН', u'ОНО', u'ЕГО'])
        self.check_norm(u'ЕМУ', [u'ОН', u'ОНО'])

    def testNoBase(self):
        self.check_norm(u'НАИНЕВЕРОЯТНЕЙШИЙ', [u'ВЕРОЯТНЫЙ'])
        self.check_norm(u'ЛУЧШИЙ', [u'ХОРОШИЙ'])
        self.check_norm(u'НАИЛУЧШИЙ', [u'ХОРОШИЙ'])
        self.check_norm(u'ЧЕЛОВЕК', [u'ЧЕЛОВЕК'])
        self.check_norm(u'ЛЮДИ', [u'ЧЕЛОВЕК'])

    def testPredict(self):
        self.check_norm(u'ТРИЖДЫЧЕРЕЗПИЛЮЛЮОКНАМИ', [u'ТРИЖДЫЧЕРЕЗПИЛЮЛЮОКНА'])
        self.check_norm(u'РАЗКВАКАЛИСЬ',[u'РАЗКВАКАТЬСЯ'])
        self.check_norm(u'КАШИВАРНЕЕ',[u'КАШИВАРНЫЙ'])
        self.check_norm(u'ДЕПЫРТАМЕНТОВ',[u'ДЕПЫРТАМЕНТ'])
        self.check_norm(u'ИЗМОХРАТИЛСЯ',[u'ИЗМОХРАТИТЬСЯ'])

    def testNoProdClassesInPrediction(self):
        self.check_norm(u'БУТЯВКОЙ',[u'БУТЯВКА']) # и никаких местоимений!
        self.check_norm(u'САПАЮТ',[u'САПАТЬ']) # и никаких местоимений!


class TestMorphPickle(TestMorphShelve):
    morph_ru = pymorphy.get_pickle_morph('ru')#, use_psyco = False)
    morph_en = pymorphy.get_pickle_morph('en')#, use_psyco = False)

if __name__ == '__main__':
    unittest.main()

