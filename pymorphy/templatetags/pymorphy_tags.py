#coding: utf-8

import re
from django import template

from pymorphy.django_conf import default_morph, MARKER_OPEN, MARKER_CLOSE
from pymorphy.split import split_into_words, space_regex

register = template.Library()

markup_re = re.compile('(%s.+?%s)' % (MARKER_OPEN, MARKER_CLOSE), re.U)

def _restore_register(morphed_word, word):
    """ Восстановить регистр слова """
    if '-' in word:
        parts = zip(morphed_word.split('-'), word.split('-'))
        return '-'.join(_restore_register(*p) for p in parts)
    if word.isupper():
        return morphed_word.upper()
    elif word[0].isupper():
        return morphed_word[0].upper() + morphed_word[1:].lower()
    else:
        return morphed_word.lower()

def _process_phrase(phrase, process_func, *args, **kwargs):
    """ обработать фразу """
    words = split_into_words(phrase)
    result=""
    try:
        for word in words:
            if space_regex.match(word):
                result += word
                continue
            processed = process_func(word.upper(), *args, **kwargs)
            processed = _restore_register(processed, word) if processed else word
            result += processed
    except:
        return phrase
    return result


def _process_marked_phrase(phrase, process_func, *args, **kwargs):
    """ Обработать фразу. В фразе обрабатываются только куски, заключенные
        в двойные квадратные скобки (например, "[[лошадь]] Пржевальского").
    """
    def process(m):
        return _process_phrase(m.group(1)[2:-2],
                               process_func, *args, **kwargs)
    return re.sub(markup_re, process, phrase)


def _process_unmarked_phrase(phrase, process_func, *args, **kwargs):
    """ Обработать фразу. В фразе не обрабатываются куски, заключенные
        в двойные квадратные скобки (например, "лошадь [[Пржевальского]]").
    """
    def process(part):
        if not re.match(markup_re, part):
            return _process_phrase(part, process_func, *args, **kwargs)
        return part[2:-2]

    parts = [process(s) for s in re.split(markup_re, phrase)]
    return "".join(parts)


@register.filter
def inflect(phrase, form):
    if not phrase:
        return phrase
    return _process_unmarked_phrase(unicode(phrase), default_morph.inflect_ru, form)

@register.filter
def inflect_marked(phrase, form):
    if not phrase:
        return phrase
    return _process_marked_phrase(unicode(phrase), default_morph.inflect_ru, form)

@register.filter
def plural(phrase, amount):
    if not phrase:
        return phrase
    return _process_unmarked_phrase(phrase, default_morph.pluralize_inflected_ru, amount)

