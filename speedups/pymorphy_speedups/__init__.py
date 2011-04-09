#coding: utf-8
from pymorphy_speedups.version import *

def setup_psyco():
    ''' Попытаться оптимизировать узкие места с помощью psyco '''
    try:
        import psyco
        from pymorphy.backends.shelve_source.shelf_with_hooks import ShelfWithHooks
        from pymorphy.morph import Morph, GramForm, _get_split_variants

        psyco.bind(Morph._get_graminfo)
        psyco.bind(Morph._get_lemma_graminfo)
        psyco.bind(GramForm.__init__)
        psyco.bind(ShelfWithHooks._getitem__cached)
        psyco.bind(ShelfWithHooks._contains__cached)
        psyco.bind(_get_split_variants)
    except ImportError:
        pass
