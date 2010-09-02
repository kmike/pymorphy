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



if __name__ == '__main__':
    unittest.main()
