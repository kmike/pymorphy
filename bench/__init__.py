#coding: utf-8

import cProfile
from datetime import datetime
import re
import os
import codecs
from pympler.muppy.muppy import get_objects, get_size

import pymorphy

DICT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '..', 'dicts', 'converted'))


def get_words(text):
    r = re.compile('[\W+-]',re.U)
    return [word for word in r.split(text.upper()) if word]


def do_normalize(words, morph):
    for word in words:
        forms = morph.normalize(word)


def do_pluralize(words, morph):
    for word in words:
        forms = morph.pluralize_ru(word)


def do_all(words, morph):
    do_normalize(words, morph)
    do_pluralize(words, morph)


def print_memory_diff():
    return
    usage = get_size(get_objects())
    if print_memory_diff._usage:
        print u"Memory usage diff: %d Kb" % ((usage-print_memory_diff._usage)/1024)
    else:
        print u"Memory usage: %d Kb" % (usage/1024)
    print_memory_diff._usage = usage
print_memory_diff._usage = None


def load_words(fn):
    filename = os.path.abspath(os.path.join('text', fn))
    f = codecs.open(filename, encoding='utf-8')
    text = f.read()
    f.close()
    return get_words(text)


def bench(file, backend='shelve', use_psyco=True, use_cache=True):

    words = load_words(file)
    print 'Text is loaded (%d words)' % len(words)
    print_memory_diff()

    if use_psyco:
        pymorphy.setup_psyco()

    if backend == 'pickle':
        morph = pymorphy.morph.get_pickle_morph('ru')
    else:
        morph = pymorphy.get_morph(os.path.join(DICT_PATH,'ru'), backend, cached = use_cache)

    cProfile.runctx('do_all(words, morph)', globals = globals(), locals=locals())
    print_memory_diff()



