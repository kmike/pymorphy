#coding: utf-8
from __future__ import unicode_literals
from pymorphy.morph_tests.base import unittest2
from pymorphy.morph import GramForm

class GramFormTest(unittest2.TestCase):

    def test_from_str(self):
        form = GramForm('мн,рд')
        self.assertTrue('рд' in form.form)
        self.assertTrue('мн' in form.form)

    def test_form_change(self):
        form = GramForm('мн,рд,мр')
        form.update('дт')
        self.assertTrue('дт' in form.form)
        self.assertTrue('мн' in form.form)
        self.assertFalse('рд' in form.form)

    def test_multi_form_change(self):
        form = GramForm('мн,рд,мр')
        form.update('дт,ед')
        self.assertTrue('дт' in form.form)
        self.assertTrue('ед' in form.form)
        self.assertFalse('рд' in form.form)
        self.assertFalse('мн' in form.form)

    def test_form_str(self):
        form = GramForm('мр,мн,рд')
        self.assertTrue(form.get_form_string().count('мр') == 1)
        self.assertTrue(form.get_form_string().count('мн') == 1)
        self.assertTrue(form.get_form_string().count('рд') == 1)
        self.assertTrue(len(form.get_form_string()) == (2*3)+2)
        form.update('дт')
        self.assertTrue(form.get_form_string().count('мр') == 1)
        self.assertTrue(form.get_form_string().count('мн') == 1)
        self.assertTrue(form.get_form_string().count('дт') == 1)
        self.assertTrue(len(form.get_form_string()) == (2*3)+2)

    def test_match(self):
        form = GramForm("мр,ед,имя")
        self.assertTrue(form.match(GramForm("мр")))
        self.assertTrue(form.match(GramForm("ед,мр")))

    def test_match_inverted(self):
        form = GramForm("мр,ед,имя")
        self.assertFalse(form.match(GramForm("мр,!имя")))
        self.assertTrue(form.match(GramForm("ед,!тв")))

    def test_match_string(self):
        form = GramForm('мр,ед,им')
        self.assertEqual(form.match_string('мр'), 'мр')
        self.assertEqual(form.match_string('ед'), 'ед')
        self.assertEqual(form.match_string('им'), 'им')
        self.assertEqual(form.match_string('!имя'), '!имя')
        self.assertFalse(form.match_string('жр'))

