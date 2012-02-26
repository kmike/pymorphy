# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from pymorphy.morph_tests.base import unittest2, MorphTestCase
from pymorphy.contrib.word_case import restore_word_case

class RestoreCaseTest(MorphTestCase):

    def assertRestored(self, word, original_word, result):
        self.assertEqualRu(restore_word_case(word, original_word), result)

    def test_upper(self):
        self.assertRestored('ЛЮДИ', 'ЧЕЛОВЕК', 'ЛЮДИ')

    def test_lower(self):
        self.assertRestored('ЛЮДИ', 'человек', 'люди')

    def test_title(self):
        self.assertRestored('ЛЮДИ', 'Человек', 'Люди')

    def test_hyphenated(self):
        self.assertRestored('ЛЮДИ-ГОРЫ-МАЛЕНЬКИЙ', 'Человек-ГОРА-небольшая', 'Люди-ГОРЫ-маленький')

    # сейчас не поддерживается, т.к. неясен алгоритм
    @unittest2.expectedFailure
    def test_mixed(self):
        self.assertRestored('ЛюДи', 'ЛюДи', 'ЛюДи')

if __name__ == '__main__':
    unittest2.main()
