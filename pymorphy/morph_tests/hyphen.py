#coding: utf-8

import unittest

from dicts import morph_ru

class TestHyphen(unittest.TestCase):

    def assertHasInfo(self, word, norm, cls, method, scan=False):
        is_correct = lambda form: (method in form['method']) and (form['norm'] == norm) and (form['class'] == cls)
        if scan:
            forms = morph_ru.get_graminfo_scan(word)
        else:
            forms = morph_ru.get_graminfo(word)
        self.assertTrue(any([is_correct(form) for form in forms]))

    def testDict(self):
        self.assertHasInfo(u'САНКТ-ПЕТЕРБУРГА', u'САНКТ-ПЕТЕРБУРГ', u'С', u'lemma(С).suffix(АНКТ-ПЕТЕРБУРГА)')

    def testImmutableLeft(self):
        self.assertHasInfo(u'ИНТЕРНЕТ-МАГАЗИНА', u'ИНТЕРНЕТ-МАГАЗИН', u'С', u'hyphen-prefix')
        self.assertHasInfo(u'PDF-ДОКУМЕНТОВ', u'PDF-ДОКУМЕНТ', u'С', u'hyphen-prefix')
        self.assertHasInfo(u'АММИАЧНО-СЕЛИТРОВОГО', u'АММИАЧНО-СЕЛИТРОВЫЙ', u'П', u'hyphen-prefix')

    def testMutableLeft(self):
        self.assertHasInfo(u'БЫСТРО-БЫСТРО', u'БЫСТРО-БЫСТРО', u'Н', u'word-formation')
        self.assertHasInfo(u'КОМАНД-УЧАСТНИЦ', u'КОМАНДА-УЧАСТНИЦА', u'С', u'word-formation')
        self.assertHasInfo(u'БЕГАЕТ-ПРЫГАЕТ', u'БЕГАТЬ-ПРЫГАТЬ', u'Г', u'word-formation')
        self.assertHasInfo(u'ДУЛ-НАДУВАЛСЯ', u'ДУТЬ-НАДУВАТЬСЯ', u'Г', u'word-formation')

    def testScan(self):
        self.assertHasInfo(u'ИНТЕРНЕТ-МАГJЗИНА', u'ИНТЕРНЕТ-МАГАЗИН', u'С', u'hyphen-prefix', True)
        self.assertHasInfo(u'PDF-ДФКУМЕНТ0В', u'PDF-ДОКУМЕНТ', u'С', u'hyphen-prefix', True)
        self.assertHasInfo(u'АММИАЧНФ-СЕЛИТР0ВФГО', u'АММИАЧНО-СЕЛИТРОВЫЙ', u'П', u'hyphen-prefix', True)
        self.assertHasInfo(u'БЫСТРО-БЫСТРФ', u'БЫСТРО-БЫСТРО', u'Н', u'word-formation', True)

    def testScanDict(self):
        self.assertHasInfo(u'САНКТ-ПЕТЕРБУРГ4', u'САНКТ-ПЕТЕРБУРГ', u'С', u'lemma(С).suffix(АНКТ-ПЕТЕРБУРГА)', True)
        self.assertHasInfo(u'КJКИХ-ТО', u'КАКОЙ-ТО', u'МС-П', u'suffix(ИХ-ТО)', True)

    def testScanErrorInLeft(self):
        self.assertHasInfo(u'КОМJНД-УЧАСТНИЦ', u'КОМАНДА-УЧАСТНИЦА', u'С', u'word-formation', True)

    def testScanNoError(self):
        self.assertHasInfo(u'ФЕСТИВАЛЬ-КОНКУРС', u'ФЕСТИВАЛЬ-КОНКУРС', u'С', u'word-formation', True)

    def testScanNeedsLeftPrediction(self):
        self.assertHasInfo(u'КОВАБJНД-УЧАСТНИЦ', u'КОВАБАНДА-УЧАСТНИЦА', u'С', u'word-formation', True)


if __name__ == '__main__':
    unittest.main()