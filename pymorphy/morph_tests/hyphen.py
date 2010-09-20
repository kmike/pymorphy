#coding: utf-8
import unittest
from pymorphy.morph_tests.base import MorphTestCase

class TestHyphen(MorphTestCase):

    def test_dict(self):
        self.assertHasInfo(u'САНКТ-ПЕТЕРБУРГА', u'САНКТ-ПЕТЕРБУРГ', u'С', u'lemma(С).suffix(АНКТ-ПЕТЕРБУРГА)')

    def test_immutable_left(self):
        self.assertHasInfo(u'ИНТЕРНЕТ-МАГАЗИНА', u'ИНТЕРНЕТ-МАГАЗИН', u'С', u'hyphen-prefix')
        self.assertHasInfo(u'PDF-ДОКУМЕНТОВ', u'PDF-ДОКУМЕНТ', u'С', u'hyphen-prefix')
        self.assertHasInfo(u'АММИАЧНО-СЕЛИТРОВОГО', u'АММИАЧНО-СЕЛИТРОВЫЙ', u'П', u'hyphen-prefix')

    def test_mutable_left(self):
        self.assertHasInfo(u'БЫСТРО-БЫСТРО', u'БЫСТРО-БЫСТРО', u'Н', u'word-formation')
        self.assertHasInfo(u'КОМАНД-УЧАСТНИЦ', u'КОМАНДА-УЧАСТНИЦА', u'С', u'word-formation')
        self.assertHasInfo(u'БЕГАЕТ-ПРЫГАЕТ', u'БЕГАТЬ-ПРЫГАТЬ', u'Г', u'word-formation')
        self.assertHasInfo(u'ДУЛ-НАДУВАЛСЯ', u'ДУТЬ-НАДУВАТЬСЯ', u'Г', u'word-formation')

    def test_extra_prefix(self):
        self.assertHasInfo(u'ПОЧТОВО-БАНКОВСКИЙ', u'ПОЧТОВО-БАНКОВСКИЙ', u'П', u'hyphen-prefix(ПОЧТОВО)')
        self.assertHasInfo(u'ПО-ПРЕЖНЕМУ', u'ПО-ПРЕЖНЕМУ', u'Н', u'lemma(ПО-ПРЕЖНЕМУ)')
        self.assertHasInfo(u'ПО-ПРЕЖНЕМУ', u'ПРЕЖНИЙ', u'П', u'hyphen-prefix()')

    def test_train_bug(self):
        self.assertHasInfo(u'ПОЕЗДОВ-ЭКСПРЕССОВ', u'ПОЕЗД-ЭКСПРЕСС', u'С', u'word-formation')
        self.assertHasInfo(u'ПОДРОСТКАМИ-ПРАКТИКАНТАМИ', u'ПОДРОСТОК-ПРАКТИКАНТ')
        self.assertHasInfo(u'ПОДВОДНИКОВ-СЕВЕРОМОРЦЕВ', u'ПОДВОДНИК-СЕВЕРОМОРЕЦ', u'С', u'word-formation')

    def test_strip_hyphens(self):
        self.assertStandard(u'ПО-ПРЕЖНЕМУ', u'ПРЕЖНИЙ')
        self.assertStandard(u'ПО-ПРЕЖНЕМУ', u'ПРЕЖНИЙ', scan=True)

    def test_rostov(self):
        self.assertStandard(u'РОСТОВЕ-НА-ДОНУ', u'РОСТОВ-НА-ДОНУ')

class InflectHyphenTest(MorphTestCase):

    def test_inflect_prefix(self):
        self.assertInflected(u'ИНТЕРНЕТ-МАГАЗИН', u'дт,мн', u'ИНТЕРНЕТ-МАГАЗИНАМ')

    def test_inflect_word_formation(self):
        self.assertInflected(u'ЧЕЛОВЕК-ГОРА', u'дт,ед', u'ЧЕЛОВЕКУ-ГОРЕ')

    def test_inflect_rostov(self):
        self.assertInflected(u'РОСТОВ-НА-ДОНУ', u'пр', u'РОСТОВЕ-НА-ДОНУ')


class PluralHyphenTest(MorphTestCase):

    def test_plural(self):
        self.assertPlural(u'ИНТЕРНЕТ-МАГАЗИН', u'ИНТЕРНЕТ-МАГАЗИНЫ')

    def test_plural_word_formation(self):
        self.assertPlural(u'ЧЕЛОВЕК-ГОРА', u'ЛЮДИ-ГОРЫ')

if __name__ == '__main__':
    unittest.main()
