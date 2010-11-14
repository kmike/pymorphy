#coding: utf-8
from pymorphy.morph_tests.base import unittest2
from pymorphy.split import split_into_words

class SplitTest(unittest2.TestCase):

    def assertSplitted(self, text, words):
        self.assertEqual(split_into_words(text), words)

    def test_split_simple(self):
        self.assertSplitted(u'Мама мыла раму', [u'Мама', ' ', u'мыла', ' ', u'раму'])
        self.assertSplitted(u'Постой, паровоз!', [u'Постой', ',', ' ', u'паровоз', '!'])

    def test_split_hyphen(self):
        self.assertSplitted(u'Ростов-на-Дону', [u'Ростов-на-Дону'])
        self.assertSplitted(u'Ура - победа', [u'Ура', ' ', '-', ' ', u'победа'])

    def test_split_signs(self):
        self.assertSplitted(u'a+b=c_1', ['a','+','b','=','c_1'])

if __name__ == '__main__':
    unittest2.main()
