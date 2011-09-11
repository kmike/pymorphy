#coding: utf-8
from pymorphy.morph_tests.base import unittest2
from pymorphy.morph import GramForm

class GramFormTest(unittest2.TestCase):

    def test_from_str(self):
        form = GramForm(u'мн,рд')
        self.assertTrue(u'рд' in form.form)
        self.assertTrue(u'мн' in form.form)

    def test_form_change(self):
        form = GramForm(u'мн,рд,мр')
        form.update(u'дт')
        self.assertTrue(u'дт' in form.form)
        self.assertTrue(u'мн' in form.form)
        self.assertFalse(u'рд' in form.form)

    def test_multi_form_change(self):
        form = GramForm(u'мн,рд,мр')
        form.update(u'дт,ед')
        self.assertTrue(u'дт' in form.form)
        self.assertTrue(u'ед' in form.form)
        self.assertFalse(u'рд' in form.form)
        self.assertFalse(u'мн' in form.form)

    def test_form_str(self):
        form = GramForm(u'мр,мн,рд')
        self.assertTrue(form.get_form_string().count(u'мр') == 1)
        self.assertTrue(form.get_form_string().count(u'мн') == 1)
        self.assertTrue(form.get_form_string().count(u'рд') == 1)
        self.assertTrue(len(form.get_form_string()) == (2*3)+2)
        form.update(u'дт')
        self.assertTrue(form.get_form_string().count(u'мр') == 1)
        self.assertTrue(form.get_form_string().count(u'мн') == 1)
        self.assertTrue(form.get_form_string().count(u'дт') == 1)
        self.assertTrue(len(form.get_form_string()) == (2*3)+2)

    def test_match(self):
        form = GramForm(u"мр,ед,имя")
        self.assertTrue(form.match(GramForm(u"мр")))
        self.assertTrue(form.match(GramForm(u"ед,мр")))

    def test_match_inverted(self):
        form = GramForm(u"мр,ед,имя")
        self.assertFalse(form.match(GramForm(u"мр,!имя")))
        self.assertTrue(form.match(GramForm(u"ед,!тв")))
    
    def test_match_string(self):
        form = GramForm(u'мр,ед,им')
        self.assertEqual(form.match_string(u'мр'), u'мр')
        self.assertEqual(form.match_string(u'ед'), u'ед')
        self.assertEqual(form.match_string(u'им'), u'им')
        self.assertEqual(form.match_string(u'!имя'), u'!имя')
        self.assertFalse(form.match_string(u'жр'))

