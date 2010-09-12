#coding: utf-8

import unittest
from dicts import morph_ru
from pymorphy.morph_tests.base import MorphTestCase

class TestPluraliseRu(MorphTestCase):

    def test_nouns(self):
        self.assertPlural(u'ГОРОД', u'ГОРОДА')
        self.assertPlural(u'СТАЛЬ', u'СТАЛИ')
        self.assertPlural(u'СТАЛЕВАРОМ', u'СТАЛЕВАРАМИ')

    def test_predictor_nouns(self):
        self.assertPlural(u'БУТЯВКОЙ', u'БУТЯВКАМИ')

    def test_verbs(self):
        self.assertPlural(u'ГУЛЯЛ', u'ГУЛЯЛИ')
        self.assertPlural(u'ГУЛЯЛА', u'ГУЛЯЛИ')
        self.assertPlural(u'РАСПРЫГИВАЕТСЯ', u'РАСПРЫГИВАЮТСЯ')

    def test_prefix(self):
        self.assertPlural(u'СУПЕРКОТ', u'СУПЕРКОТЫ')

    def test_predict_by_suffix(self):
        self.assertPlural(u'ДЕПЫРТАМЕНТ', u'ДЕПЫРТАМЕНТЫ')
        self.assertPlural(u'ХАБР', u'ХАБРЫ')

    def test_invalid_word(self):
        self.assertPlural(u'123', u'123')

    def test_invalid_graminfo(self):
        self.assertPlural(u'НАЧАЛО', u'НАЧАЛА', gram_class=u'С')


class TestInflectRu(MorphTestCase):

    def test_inflect(self):
        self.assertInflected(u"СУСЛИКОВ", u"дт", u"СУСЛИКАМ")
        self.assertInflected(u"СУСЛИК", u"дт", u"СУСЛИКУ")
        self.assertInflected(u"СУСЛИКА", u"дт", u"СУСЛИКУ")
        self.assertInflected(u"СУСЛИК", u"мн,дт", u"СУСЛИКАМ")

    def test_verbs(self):
        self.assertInflected(u"ГУЛЯЮ", u"прш", u"ГУЛЯЛ")
        self.assertInflected(u"ГУЛЯЛ", u"нст", u"ГУЛЯЮ")


class TestPluralizeInflected(MorphTestCase):

    def assertInflectedPlural(self, word, count, result, *args, **kwargs):
        morphed_word = morph_ru.pluralize_inflected_ru(word, count, *args, **kwargs)
        self.assertEqualRu(morphed_word, result)

    def test_parrots(self):
        self.assertInflectedPlural(u"ПОПУГАЙ", 1, u"ПОПУГАЙ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 2, u"ПОПУГАЯ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 3, u"ПОПУГАЯ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 4, u"ПОПУГАЯ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 5, u"ПОПУГАЕВ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 7, u"ПОПУГАЕВ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 9, u"ПОПУГАЕВ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 0, u"ПОПУГАЕВ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 10, u"ПОПУГАЕВ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 11, u"ПОПУГАЕВ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 12, u"ПОПУГАЕВ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 15, u"ПОПУГАЕВ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 19, u"ПОПУГАЕВ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 21, u"ПОПУГАЙ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 32, u"ПОПУГАЯ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 38, u"ПОПУГАЕВ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 232, u"ПОПУГАЯ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 111, u"ПОПУГАЕВ")
        self.assertInflectedPlural(u"ПОПУГАЙ", 101, u"ПОПУГАЙ")

    def test_butyavka(self):
        self.assertInflectedPlural(u"БУТЯВКА", 1, u"БУТЯВКА")
        self.assertInflectedPlural(u"БУТЯВКА", 2, u"БУТЯВКИ")
        self.assertInflectedPlural(u"БУТЯВКА", 5, u"БУТЯВОК")

if __name__ == '__main__':
    unittest.main()
