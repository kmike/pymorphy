#coding: utf-8

import unittest

from dicts import morph_ru
from pymorphy.morph_tests.base import MorphTestCase

class TestScans(MorphTestCase):

    def testBasic(self):
        self.assert_has_info(u'РАСШИФР0ВКИ', u'РАСШИФРОВКА', u'С', scan=True)

    def testJunkyVariantsBug(self):
        self.assert_has_info(u'КАБИНЕТ', u'КАБИНЕТ', u'С', scan=True, )
#        self.assert_has_info(u'КАБИНЕТЫ', u'КАБИНЕТЫ', u'С', scan=True)




if __name__ == '__main__':
    unittest.main()