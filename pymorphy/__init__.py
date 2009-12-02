#coding: utf8

from pymorphy.morph import get_pickle_morph, get_shelve_morph, setup_psyco

if __name__ == '__main__':
    m = get_shelve_morph('ru')
#    m.get_graminfo(u"МОСКВА")
    for form in m.get_graminfo(u'НАИНЕВЕРОЯТНЕЙШИЙ'):
        for v in form:
            print v, form[v]
        print '----'

