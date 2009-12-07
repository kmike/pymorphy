#coding: utf-8

from unittest import TestCase

from templatetags.pymorphy_tags import inflect

class InflectTagTest(TestCase):

    def assertInflected(self, phrase, form, result):
        inflected_word = inflect(phrase, form)
        self.assertEqual(inflected_word, result, u"%s != %s" % (inflected_word, result))

    def testWordCase(self):
        self.assertInflected(u'Котопес', '', u'Котопес')
        self.assertInflected(u'ВАСЯ', '', u'ВАСЯ')
        self.assertInflected(u'котопес', '', u'котопес')

    def testOneWord(self):
        self.assertInflected(u'Москва', u'пр', u'Москве')
        self.assertInflected(u'бутявка', u'мн,тв', u'бутявками')
        self.assertInflected(u'Петрович', u'дт,отч', u'Петровичу')

    def testSusliki(self):
        self.assertInflected(u'сусликов', u'тв', u'сусликами')

    def testComplexPhrase(self):
        self.assertInflected(u'тридцать восемь попугаев и Удав', u'дт',
                             u'тридцати восьми попугаям и Удаву')
        self.assertInflected(u'Пятьдесят девять сусликов', u'тв', u'Пятьюдесятью девятью сусликами')

    def testName(self):
        self.assertInflected(u'Геннадий Петрович', u'вн', u'Геннадия Петровича')
        self.assertInflected(u'Геннадий Петрович', u'дт', u'Геннадию Петровичу')
        self.assertInflected(u'Геннадий Петрович', u'тв', u'Геннадием Петровичем')
        self.assertInflected(u'Геннадий Петрович', u'пр', u'Геннадии Петровиче')

