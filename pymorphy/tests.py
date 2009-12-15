#coding: utf-8

from unittest import TestCase

from templatetags.pymorphy_tags import inflect, plural

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


    # тесты для несклоняемых кусков
    def testBasicNoinflect(self):
        self.assertInflected(u'лошадь [[Пржевальского]]', u'дт', u'лошади Пржевальского')
        self.assertInflected(u'[[Москва]]', u'пр', u'Москва')
        self.assertInflected(u'Москва', u'пр', u'Москве')
        self.assertInflected(u'Москва[[-сити]]', u'пр', u'Москве-сити')

    def testTwoWordsNoinflect(self):
        self.assertInflected(u'лошадь [[Пржевальского]] и красный конь [[Кузьмы Петрова-Водкина]]',
                             u'дт',
                             u'лошади Пржевальского и красному коню Кузьмы Петрова-Водкина')



class PluralTagTest(TestCase):
    def assertPlural(self, phrase, amount, result):
        morphed = plural(phrase, amount)
        self.assertEqual(morphed, result, u"%s != %s" % (morphed, result))

    def testPluralize(self):
        self.assertPlural(u'бутявка', 1, u'бутявка')
        self.assertPlural(u'бутявка', 2, u'бутявки')
        self.assertPlural(u'бутявка', 5, u'бутявок')
        self.assertPlural(u'Бутявка', 1, u'Бутявка')

    def testPhrase(self):
        self.assertPlural(u'Геннадий Петрович', 8, u'Геннадиев Петровичей')
