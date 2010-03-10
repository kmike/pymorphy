#coding: utf-8
import unittest
from pymorphy.morph_tests.base import MorphTestCase

class TestHyphen(MorphTestCase):

    def testDict(self):
        self.assert_has_info(u'САНКТ-ПЕТЕРБУРГА', u'САНКТ-ПЕТЕРБУРГ', u'С', u'lemma(С).suffix(АНКТ-ПЕТЕРБУРГА)')

    def testImmutableLeft(self):
        self.assert_has_info(u'ИНТЕРНЕТ-МАГАЗИНА', u'ИНТЕРНЕТ-МАГАЗИН', u'С', u'hyphen-prefix')
        self.assert_has_info(u'PDF-ДОКУМЕНТОВ', u'PDF-ДОКУМЕНТ', u'С', u'hyphen-prefix')
        self.assert_has_info(u'АММИАЧНО-СЕЛИТРОВОГО', u'АММИАЧНО-СЕЛИТРОВЫЙ', u'П', u'hyphen-prefix')

    def testMutableLeft(self):
        self.assert_has_info(u'БЫСТРО-БЫСТРО', u'БЫСТРО-БЫСТРО', u'Н', u'word-formation')
        self.assert_has_info(u'КОМАНД-УЧАСТНИЦ', u'КОМАНДА-УЧАСТНИЦА', u'С', u'word-formation')
        self.assert_has_info(u'БЕГАЕТ-ПРЫГАЕТ', u'БЕГАТЬ-ПРЫГАТЬ', u'Г', u'word-formation')
        self.assert_has_info(u'ДУЛ-НАДУВАЛСЯ', u'ДУТЬ-НАДУВАТЬСЯ', u'Г', u'word-formation')

    def testExtraPrefix(self):
        self.assert_has_info(u'ПОЧТОВО-БАНКОВСКИЙ', u'ПОЧТОВО-БАНКОВСКИЙ', u'П', u'hyphen-prefix(ПОЧТОВО)')
        self.assert_has_info(u'ПО-ПРЕЖНЕМУ', u'ПО-ПРЕЖНЕМУ', u'Н', u'lemma(ПО-ПРЕЖНЕМУ)')
        self.assert_has_info(u'ПО-ПРЕЖНЕМУ', u'ПРЕЖНИЙ', u'П', u'hyphen-prefix()')

    def testTrainBug(self):
        self.assert_has_info(u'ПОЕЗДОВ-ЭКСПРЕССОВ', u'ПОЕЗД-ЭКСПРЕСС', u'С', u'word-formation')
        self.assert_has_info(u'ПОДРОСТКАМИ-ПРАКТИКАНТАМИ', u'ПОДРОСТОК-ПРАКТИКАНТ')
        self.assert_has_info(u'ПОДВОДНИКОВ-СЕВЕРОМОРЦЕВ', u'ПОДВОДНИК-СЕВЕРОМОРЕЦ', u'С', u'word-formation')

    def testStripHyphens(self):
        self.assert_standard(u'ПО-ПРЕЖНЕМУ', u'ПРЕЖНИЙ')
        self.assert_standard(u'ПО-ПРЕЖНЕМУ', u'ПРЕЖНИЙ', scan=True)



class HyphenScanTest(MorphTestCase):

    def testScan(self):
        self.assert_has_info(u'ИНТЕРНЕТ-МАГJЗИНА', u'ИНТЕРНЕТ-МАГАЗИН', u'С', u'hyphen-prefix', True)
        self.assert_has_info(u'PDF-ДФКУМЕНТ0В', u'PDF-ДОКУМЕНТ', u'С', u'hyphen-prefix', True)
        self.assert_has_info(u'АММИАЧНФ-СЕЛИТР0ВФГО', u'АММИАЧНО-СЕЛИТРОВЫЙ', u'П', u'hyphen-prefix', True)
        self.assert_has_info(u'БЫСТРО-БЫСТРФ', u'БЫСТРО-БЫСТРО', u'Н', u'word-formation', True)

    def testScanDict(self):
        self.assert_has_info(u'САНКТ-ПЕТЕРБУРГ4', u'САНКТ-ПЕТЕРБУРГ', u'С', u'lemma(С).suffix(АНКТ-ПЕТЕРБУРГА)', True)
        self.assert_has_info(u'КJКИХ-ТО', u'КАКОЙ-ТО', u'МС-П', u'suffix(ИХ-ТО)', True)

    def testScanErrorInLeft(self):
        self.assert_has_info(u'КОМJНД-УЧАСТНИЦ', u'КОМАНДА-УЧАСТНИЦА', u'С', u'word-formation', True)

    def testScanNoError(self):
        self.assert_has_info(u'ФЕСТИВАЛЬ-КОНКУРС', u'ФЕСТИВАЛЬ-КОНКУРС', u'С', u'word-formation', True)
        self.assert_norm(u'ФИЗИКО-ХИМИЯ', u'ФИЗИКО-ХИМИЯ', scan=True)

    def testScanNeedsLeftPrediction(self):
        self.assert_has_info(u'КОВАБJНД-УЧАСТНИЦ', u'КОВАБАНДА-УЧАСТНИЦА', u'С', u'word-formation', True)

class HyphenUtils(MorphTestCase):

    def testInflectPrefix(self):
        self.assert_inflect(u'ИНТЕРНЕТ-МАГАЗИН', u'дт,мн', u'ИНТЕРНЕТ-МАГАЗИНАМ')

    def testInflectWordFormation(self):
        self.assert_inflect(u'ЧЕЛОВЕК-ГОРА', u'дт,ед', u'ЧЕЛОВЕКУ-ГОРЕ')

    def testPlural(self):
        self.assert_plural(u'ИНТЕРНЕТ-МАГАЗИН', u'ИНТЕРНЕТ-МАГАЗИНЫ')

    def testPluralWordFormation(self):
        self.assert_plural(u'ЧЕЛОВЕК-ГОРА', u'ЛЮДИ-ГОРЫ')

if __name__ == '__main__':
    unittest.main()