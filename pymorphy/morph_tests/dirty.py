#coding: utf-8

import unittest

from dicts import morph_ru
from pymorphy.morph_tests.base import MorphTestCase

class TestScans(MorphTestCase):

    def test_basic(self):
        self.assertHasInfo(u'РАСШИФР0ВКИ', u'РАСШИФРОВКА', u'С', scan=True)

    def test_junky_variants_bug(self):
        self.assertStandard(u'КАБИНЕТЫ', u'КАБИНЕТ', u'S', form='pl')
        self.assertStandard(u'КАБИНЕТЫ', u'КАБИНЕТ', u'S', form='pl', scan=True)

        self.assertStandard(u'КАБИНЕТЫ', u'КАБИНЕТ', u'S', form='sg', has_info=False)
        self.assertStandard(u'КАБИНЕТЫ', u'КАБИНЕТ', u'S', form='sg', has_info=False, scan=True)


class HyphenScanTest(MorphTestCase):

    def test_scan(self):
        self.assertHasInfo(u'ИНТЕРНЕТ-МАГJЗИНА', u'ИНТЕРНЕТ-МАГАЗИН', u'С', u'hyphen-prefix', True)
        self.assertHasInfo(u'PDF-ДФКУМЕНТ0В', u'PDF-ДОКУМЕНТ', u'С', u'hyphen-prefix', True)
        self.assertHasInfo(u'АММИАЧНФ-СЕЛИТР0ВФГО', u'АММИАЧНО-СЕЛИТРОВЫЙ', u'П', u'hyphen-prefix', True)
        self.assertHasInfo(u'БЫСТРО-БЫСТРФ', u'БЫСТРО-БЫСТРО', u'Н', u'word-formation', True)

    def test_scan_dict(self):
        self.assertHasInfo(u'САНКТ-ПЕТЕРБУРГ4', u'САНКТ-ПЕТЕРБУРГ', u'С', u'lemma(С).suffix(АНКТ-ПЕТЕРБУРГА)', True)
        self.assertHasInfo(u'КJКИХ-ТО', u'КАКОЙ-ТО', u'МС-П', u'suffix(ИХ-ТО)', True)

    def test_scan_error_in_left(self):
        self.assertHasInfo(u'КОМJНД-УЧАСТНИЦ', u'КОМАНДА-УЧАСТНИЦА', u'С', u'word-formation', True)

    def test_scan_no_error(self):
        self.assertHasInfo(u'ФЕСТИВАЛЬ-КОНКУРС', u'ФЕСТИВАЛЬ-КОНКУРС', u'С', u'word-formation', True)
        self.assertNormal(u'ФИЗИКО-ХИМИЯ', u'ФИЗИКО-ХИМИЯ', scan=True)

    def test_scan_needs_left_prediction(self):
        self.assertHasInfo(u'КОВАБJНД-УЧАСТНИЦ', u'КОВАБАНДА-УЧАСТНИЦА', u'С', u'word-formation', True)



if __name__ == '__main__':
    unittest.main()
