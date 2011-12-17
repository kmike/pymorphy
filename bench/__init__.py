#coding: utf-8
from __future__ import absolute_import, unicode_literals, print_function
import cProfile
from datetime import datetime
import re
import os
import codecs
import timeit

import pymorphy
from pymorphy.contrib.tokenizers import extract_words

DICT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '..', 'dicts', 'converted'))

def total_seconds(delta):
    return delta.days * 3600 * 24 + delta.seconds + delta.microseconds/100000.0


def get_words(text):
#    return list(extract_words(text))
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
#    do_pluralize(words, morph)


def print_memory_diff():
    return
    from pympler.muppy import get_objects, get_size
    usage = get_size(get_objects())
    if print_memory_diff._usage:
        print ("Memory usage diff: %d Kb" % ((usage-print_memory_diff._usage)/1024))
    else:
        print ("Memory usage: %d Kb" % (usage/1024))
    print_memory_diff._usage = usage
print_memory_diff._usage = None


def load_words(fn):
    filename = os.path.abspath(os.path.join('text', fn))
    f = codecs.open(filename, encoding='utf-8')
    text = f.read()
    f.close()
    return get_words(text)

def get_morph(backend, **kwargs):
    if backend == 'pickle':
        path = os.path.join(DICT_PATH, 'ru', 'morphs.pickle')
    else:
        path = os.path.join(DICT_PATH,'ru')
    return pymorphy.get_morph(path, backend, **kwargs)


def bench(filename, backend='shelve', use_psyco=True, use_cache=True, profile=True):

    if profile:
        words = load_words(filename)
        print ('Text is loaded (%d words)' % len(words))
        print_memory_diff()

        morph = get_morph(backend, cached=use_cache)

        prof = cProfile.Profile()
        prof = prof.runctx('do_all(words, morph)', globals = globals(), locals=locals())
        prof.print_stats(1)
    else:
#        prep = """
#from bench import do_all, load_words, get_morph
#words = load_words('%s')
#morph = get_morph('%s', cached=%s)
#        """ % (file, backend, use_cache)
#        res = timeit.timeit('do_all(words, morph)', prep, number=1)
#        print '%s => %s (cache: %s) => %.2f sec' % (file, backend, use_cache, res)

        start = datetime.now()
        words = load_words(filename)
        morph = get_morph(backend, cached=use_cache)
        loaded = datetime.now()
        do_all(words, morph)
        parsed = datetime.now()

        load_time = total_seconds(loaded-start)
        parse_time = total_seconds(parsed-loaded)
        wps = len(words)/parse_time

        print ('%s => %s (cache: %s) => load: %.2f sec, parse: %0.2f sec (%d words/sec)' % (
            filename, backend, use_cache, load_time, parse_time, wps))

    print_memory_diff()



