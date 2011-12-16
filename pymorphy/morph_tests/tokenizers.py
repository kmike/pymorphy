#coding: utf-8
from __future__ import absolute_import, unicode_literals
from pymorphy.morph_tests.base import unittest2
from pymorphy.contrib.tokenizers import extract_tokens, extract_words

class SplitTest(unittest2.TestCase):

    def assertSplitted(self, text, words):
        self.assertEqual(list(extract_tokens(text)), words)

    def test_split_simple(self):
        self.assertSplitted('Мама мыла раму', ['Мама', ' ', 'мыла', ' ', 'раму'])
        self.assertSplitted('Постой, паровоз!', ['Постой', ',', ' ', 'паровоз', '!'])

    def test_split_hyphen(self):
        self.assertSplitted('Ростов-на-Дону', ['Ростов-на-Дону'])
        self.assertSplitted('Ура - победа', ['Ура', ' ', '-', ' ', 'победа'])

    def test_split_signs(self):
        self.assertSplitted('a+b=c_1', ['a','+','b','=','c_1'])


class ExtractWordsTest(unittest2.TestCase):

    def test_exctract_words(self):
        txt = '''Это  отразилось: на количественном,и на качествен_ном
                - росте карельско-финляндского сотрудничества - офигеть! кони+лошади=масло.
                -сказал кто-то --нет--'''
        words = list(extract_words(txt))
        self.assertListEqual(words, [
            'Это', 'отразилось', 'на', 'количественном', 'и', 'на',
            'качествен_ном', 'росте', 'карельско-финляндского',
            'сотрудничества', 'офигеть', 'кони', 'лошади', 'масло',
            'сказал', 'кто-то', 'нет',
        ])

if __name__ == '__main__':
    unittest2.main()
