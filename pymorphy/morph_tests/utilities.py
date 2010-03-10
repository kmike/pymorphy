#coding: utf-8

import unittest
from dicts import morph_ru
from pymorphy.morph_tests.base import MorphTestCase

class TestPluraliseRu(MorphTestCase):

# работающие тесты ============================
    def testNouns(self):
        self.assert_plural(u'ГОРОД', u'ГОРОДА')
        self.assert_plural(u'СТАЛЬ', u'СТАЛИ')
        self.assert_plural(u'СТАЛЕВАРОМ', u'СТАЛЕВАРАМИ')

    def testPredictorNouns(self):
        self.assert_plural(u'БУТЯВКОЙ', u'БУТЯВКАМИ')

    def testVerbs(self):
        self.assert_plural(u'ГУЛЯЛ', u'ГУЛЯЛИ')
        self.assert_plural(u'ГУЛЯЛА', u'ГУЛЯЛИ')
        self.assert_plural(u'РАСПРЫГИВАЕТСЯ', u'РАСПРЫГИВАЮТСЯ')

    def testPrefix(self):
        self.assert_plural(u'СУПЕРКОТ', u'СУПЕРКОТЫ')

    def testPredictBySuffix(self):
        self.assert_plural(u'ДЕПЫРТАМЕНТ', u'ДЕПЫРТАМЕНТЫ')
        self.assert_plural(u'ХАБР', u'ХАБРЫ')

    def testInvalidWord(self):
        self.assert_plural(u'123', u'123')

    def testInvalidGraminfo(self):
        self.assert_plural(u'НАЧАЛО', u'НАЧАЛА', gram_class=u'С')


class TestInflectRu(MorphTestCase):

    def testInflect(self):
        self.assert_inflect(u"СУСЛИКОВ", u"дт", u"СУСЛИКАМ")
        self.assert_inflect(u"СУСЛИК", u"дт", u"СУСЛИКУ")
        self.assert_inflect(u"СУСЛИКА", u"дт", u"СУСЛИКУ")
        self.assert_inflect(u"СУСЛИК", u"мн,дт", u"СУСЛИКАМ")

    def testVerbs(self):
        self.assert_inflect(u"ГУЛЯЮ", u"прш", u"ГУЛЯЛ")
        self.assert_inflect(u"ГУЛЯЛ", u"нст", u"ГУЛЯЮ")


class TestPluralizeInflected(unittest.TestCase):

    def assert_morph(self, word, count, result, *args, **kwargs):
        morphed_word = morph_ru.pluralize_inflected_ru(word, count, *args, **kwargs)
        self.assertEqual(morphed_word, result, u"%s != %s" % (morphed_word, result))

    def testParrots(self):
        self.assert_morph(u"ПОПУГАЙ", 1, u"ПОПУГАЙ")
        self.assert_morph(u"ПОПУГАЙ", 2, u"ПОПУГАЯ")
        self.assert_morph(u"ПОПУГАЙ", 3, u"ПОПУГАЯ")
        self.assert_morph(u"ПОПУГАЙ", 4, u"ПОПУГАЯ")
        self.assert_morph(u"ПОПУГАЙ", 5, u"ПОПУГАЕВ")
        self.assert_morph(u"ПОПУГАЙ", 7, u"ПОПУГАЕВ")
        self.assert_morph(u"ПОПУГАЙ", 9, u"ПОПУГАЕВ")
        self.assert_morph(u"ПОПУГАЙ", 0, u"ПОПУГАЕВ")
        self.assert_morph(u"ПОПУГАЙ", 10, u"ПОПУГАЕВ")
        self.assert_morph(u"ПОПУГАЙ", 11, u"ПОПУГАЕВ")
        self.assert_morph(u"ПОПУГАЙ", 12, u"ПОПУГАЕВ")
        self.assert_morph(u"ПОПУГАЙ", 15, u"ПОПУГАЕВ")
        self.assert_morph(u"ПОПУГАЙ", 19, u"ПОПУГАЕВ")
        self.assert_morph(u"ПОПУГАЙ", 21, u"ПОПУГАЙ")
        self.assert_morph(u"ПОПУГАЙ", 32, u"ПОПУГАЯ")
        self.assert_morph(u"ПОПУГАЙ", 38, u"ПОПУГАЕВ")
        self.assert_morph(u"ПОПУГАЙ", 232, u"ПОПУГАЯ")
        self.assert_morph(u"ПОПУГАЙ", 111, u"ПОПУГАЕВ")
        self.assert_morph(u"ПОПУГАЙ", 101, u"ПОПУГАЙ")

    def testButyavka(self):
        self.assert_morph(u"БУТЯВКА", 1, u"БУТЯВКА")
        self.assert_morph(u"БУТЯВКА", 2, u"БУТЯВКИ")
        self.assert_morph(u"БУТЯВКА", 5, u"БУТЯВОК")

if __name__ == '__main__':
    unittest.main()