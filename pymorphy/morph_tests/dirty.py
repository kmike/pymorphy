#coding: utf-8

import unittest

from dicts import morph_ru

class TestDirty(unittest.TestCase):

    def testDirtyParsing(self):
        forms = morph_ru.get_graminfo_scan(u'РАСШИФР0ВКИ', standard=True)
        self.assertEqual(forms[0]['norm'], u'РАСШИФРОВКА')


if __name__ == '__main__':
    unittest.main()