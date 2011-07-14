#coding: utf-8
from pymorphy.morph_tests.base import unittest2
from pymorphy.contrib.tokenizers import extract_tokens, extract_words

class SplitTest(unittest2.TestCase):

    def assertSplitted(self, text, words):
        self.assertEqual(extract_tokens(text), words)

    def test_split_simple(self):
        self.assertSplitted(u'Мама мыла раму', [u'Мама', ' ', u'мыла', ' ', u'раму'])
        self.assertSplitted(u'Постой, паровоз!', [u'Постой', ',', ' ', u'паровоз', '!'])

    def test_split_hyphen(self):
        self.assertSplitted(u'Ростов-на-Дону', [u'Ростов-на-Дону'])
        self.assertSplitted(u'Ура - победа', [u'Ура', ' ', '-', ' ', u'победа'])

    def test_split_signs(self):
        self.assertSplitted(u'a+b=c_1', ['a','+','b','=','c_1'])


class ExtractWordsTest(unittest2.TestCase):

    def test_exctract_words(self):
        txt = u'''Это  отразилось: на количественном,и на качествен_ном
                - росте карельско-финляндского сотрудничества - офигеть! кони+лошади=масло.
                -сказал кто-то --нет--'''
        words = list(extract_words(txt))
        self.assertListEqual(words, [
            u'Это', u'отразилось', u'на', u'количественном', u'и', u'на',
            u'качествен_ном', u'росте', u'карельско-финляндского',
            u'сотрудничества', u'офигеть', u'кони', u'лошади', u'масло',
            u'сказал', u'кто-то', u'нет',
        ])

if __name__ == '__main__':
    unittest2.main()
