#coding: utf-8
from unittest import TestCase
from pymorphy.morph import GramForm

class GramFormTest(TestCase):

    def testFromStr(self):
        form = GramForm(u'мн,рд')
        self.assertTrue(u'рд' in form.form)
        self.assertTrue(u'мн' in form.form)

    def testFormChange(self):
        form = GramForm(u'мн,рд,мр')
        form.update(u'дт')
        self.assertTrue(u'дт' in form.form)
        self.assertTrue(u'мн' in form.form)
        self.assertFalse(u'рд' in form.form)

    def testFormMultiChange(self):
        form = GramForm(u'мн,рд,мр')
        form.update(u'дт,ед')
        self.assertTrue(u'дт' in form.form)
        self.assertTrue(u'ед' in form.form)
        self.assertFalse(u'рд' in form.form)
        self.assertFalse(u'мн' in form.form)

    def testFormStr(self):
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

    def testMatch(self):
        form = GramForm(u"мр,ед,имя")
        self.assertTrue(form.match(GramForm(u"мр")))
        self.assertTrue(form.match(GramForm(u"ед,мр")))

    def testMatch2(self):
        form = GramForm(u"мр,ед,имя")
        self.assertFalse(form.match(GramForm(u"мр,!имя")))
        self.assertTrue(form.match(GramForm(u"ед,!тв")))

