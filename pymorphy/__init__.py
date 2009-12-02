#coding: utf8

if __name__ == '__main__':
    from pymorphy.morph import get_shelve_morph
    m = get_shelve_morph('ru')
#    m.get_graminfo(u"МОСКВА")
    for form in m.get_graminfo(u'МОСКВ'):
        for v in form:
            print v, form[v]
        print '----'

