#coding: utf-8
from __future__ import absolute_import, unicode_literals
from .base import MorphTestCase, unittest2

class TestScans(MorphTestCase):

    def test_basic(self):
        self.assertHasInfo('РАСШИФР0ВКИ', 'РАСШИФРОВКА', 'С', scan=True)

    def test_junky_variants_bug(self):
        self.assertStandard('КАБИНЕТЫ', 'КАБИНЕТ', 'S', form='pl')
        self.assertStandard('КАБИНЕТЫ', 'КАБИНЕТ', 'S', form='pl', scan=True)

        self.assertStandard('КАБИНЕТЫ', 'КАБИНЕТ', 'S', form='sg', has_info=False)
        self.assertStandard('КАБИНЕТЫ', 'КАБИНЕТ', 'S', form='sg', has_info=False, scan=True)


class HyphenScanTest(MorphTestCase):

    def test_scan(self):
        self.assertHasInfo('ИНТЕРНЕТ-МАГJЗИНА', 'ИНТЕРНЕТ-МАГАЗИН', 'С', 'hyphen-prefix', True)
        self.assertHasInfo('PDF-ДФКУМЕНТ0В', 'PDF-ДОКУМЕНТ', 'С', 'hyphen-prefix', True)
        self.assertHasInfo('АММИАЧНФ-СЕЛИТР0ВФГО', 'АММИАЧНО-СЕЛИТРОВЫЙ', 'П', 'hyphen-prefix', True)
        self.assertHasInfo('БЫСТРО-БЫСТРФ', 'БЫСТРО-БЫСТРО', 'Н', 'word-formation', True)

    def test_scan_dict(self):
        self.assertHasInfo('САНКТ-ПЕТЕРБУРГ4', 'САНКТ-ПЕТЕРБУРГ', 'С', 'lemma(С).suffix(АНКТ-ПЕТЕРБУРГА)', True)
        self.assertHasInfo('КJКИХ-ТО', 'КАКОЙ-ТО', 'МС-П', 'suffix(ИХ-ТО)', True)

    def test_scan_error_in_left(self):
        self.assertHasInfo('КОМJНД-УЧАСТНИЦ', 'КОМАНДА-УЧАСТНИЦА', 'С', 'word-formation', True)

    @unittest2.expectedFailure
    def test_scan_no_error(self):
        self.assertHasInfo('ФЕСТИВАЛЬ-КОНКУРС', 'ФЕСТИВАЛЬ-КОНКУРС', 'С', 'word-formation', True)
        self.assertNormal('ФИЗИКО-ХИМИЯ', 'ФИЗИКО-ХИМИЯ', scan=True)

    @unittest2.expectedFailure
    def test_scan_needs_left_prediction(self):
        self.assertHasInfo('КОВАБJНД-УЧАСТНИЦ', 'КОВАБАНДА-УЧАСТНИЦА', 'С', 'word-formation', True)



if __name__ == '__main__':
    unittest2.main()
