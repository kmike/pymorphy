#coding: utf-8
from __future__ import unicode_literals, absolute_import
from .base import MorphTestCase, unittest2

class TestHyphen(MorphTestCase):

    def test_dict(self):
        self.assertHasInfo('САНКТ-ПЕТЕРБУРГА', 'САНКТ-ПЕТЕРБУРГ', 'С', 'lemma(С).suffix(АНКТ-ПЕТЕРБУРГА)')

    def test_immutable_left(self):
        self.assertHasInfo('ИНТЕРНЕТ-МАГАЗИНА', 'ИНТЕРНЕТ-МАГАЗИН', 'С', 'hyphen-prefix')
        self.assertHasInfo('PDF-ДОКУМЕНТОВ', 'PDF-ДОКУМЕНТ', 'С', 'hyphen-prefix')
        self.assertHasInfo('АММИАЧНО-СЕЛИТРОВОГО', 'АММИАЧНО-СЕЛИТРОВЫЙ', 'П', 'hyphen-prefix')

    def test_mutable_left(self):
        self.assertHasInfo('БЫСТРО-БЫСТРО', 'БЫСТРО-БЫСТРО', 'Н', 'word-formation')
        self.assertHasInfo('КОМАНД-УЧАСТНИЦ', 'КОМАНДА-УЧАСТНИЦА', 'С', 'word-formation')
        self.assertHasInfo('БЕГАЕТ-ПРЫГАЕТ', 'БЕГАТЬ-ПРЫГАТЬ', 'Г', 'word-formation')
        self.assertHasInfo('ДУЛ-НАДУВАЛСЯ', 'ДУТЬ-НАДУВАТЬСЯ', 'Г', 'word-formation')

    def test_extra_prefix(self):
        self.assertHasInfo('ПОЧТОВО-БАНКОВСКИЙ', 'ПОЧТОВО-БАНКОВСКИЙ', 'П', 'hyphen-prefix(ПОЧТОВО)')
        self.assertHasInfo('ПО-ПРЕЖНЕМУ', 'ПО-ПРЕЖНЕМУ', 'Н', 'lemma(ПО-ПРЕЖНЕМУ)')
        self.assertHasInfo('ПО-ПРЕЖНЕМУ', 'ПРЕЖНИЙ', 'П', 'hyphen-prefix()')

    @unittest2.expectedFailure
    def test_train_bug(self):
        self.assertHasInfo('ПОЕЗДОВ-ЭКСПРЕССОВ', 'ПОЕЗД-ЭКСПРЕСС', 'С', 'word-formation')
        self.assertHasInfo('ПОДРОСТКАМИ-ПРАКТИКАНТАМИ', 'ПОДРОСТОК-ПРАКТИКАНТ')
        self.assertHasInfo('ПОДВОДНИКОВ-СЕВЕРОМОРЦЕВ', 'ПОДВОДНИК-СЕВЕРОМОРЕЦ', 'С', 'word-formation')

    def test_strip_hyphens(self):
        self.assertStandard('ПО-ПРЕЖНЕМУ', 'ПРЕЖНИЙ')
        self.assertStandard('ПО-ПРЕЖНЕМУ', 'ПРЕЖНИЙ', scan=True)

    def test_rostov(self):
        self.assertStandard('РОСТОВЕ-НА-ДОНУ', 'РОСТОВ-НА-ДОНУ')

class InflectHyphenTest(MorphTestCase):

    def test_inflect_prefix(self):
        self.assertInflected('ИНТЕРНЕТ-МАГАЗИН', 'дт,мн', 'ИНТЕРНЕТ-МАГАЗИНАМ')

    @unittest2.expectedFailure
    def test_inflect_word_formation(self):
        self.assertInflected('ЧЕЛОВЕК-ГОРА', 'дт,ед', 'ЧЕЛОВЕКУ-ГОРЕ')

    def test_inflect_rostov(self):
        self.assertInflected('РОСТОВ-НА-ДОНУ', 'пр', 'РОСТОВЕ-НА-ДОНУ')


class PluralHyphenTest(MorphTestCase):

    def test_plural(self):
        self.assertPlural('ИНТЕРНЕТ-МАГАЗИН', 'ИНТЕРНЕТ-МАГАЗИНЫ')

    @unittest2.expectedFailure
    def test_plural_word_formation(self):
        self.assertPlural('ЧЕЛОВЕК-ГОРА', 'ЛЮДИ-ГОРЫ')

if __name__ == '__main__':
    unittest2.main()
