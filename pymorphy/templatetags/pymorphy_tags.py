#coding: utf-8
from __future__ import unicode_literals, absolute_import
import re
from django import template

from pymorphy.py3k import text_type
from pymorphy.django_conf import default_morph, MARKER_OPEN, MARKER_CLOSE
from pymorphy.contrib import tokenizers
from pymorphy.contrib.word_case import restore_word_case

register = template.Library()

markup_re = re.compile('(%s.+?%s)' % (MARKER_OPEN, MARKER_CLOSE), re.U)

def _process_phrase(phrase, process_func, *args, **kwargs):
    """ обработать фразу """
    words = tokenizers.extract_tokens(phrase)
    result=""
    try:
        for word in words:
            if tokenizers.GROUPING_SPACE_REGEX.match(word):
                result += word
                continue
            processed = process_func(word.upper(), *args, **kwargs)
            processed = restore_word_case(processed, word) if processed else word
            result += processed
    except Exception:
        return phrase
    return result


def _process_marked_phrase(phrase, process_func, *args, **kwargs):
    """
    Обработать фразу. В фразе обрабатываются только куски, заключенные
    в двойные квадратные скобки (например, "[[лошадь]] Пржевальского").
    """
    def process(m):
        return _process_phrase(m.group(1)[2:-2],
                               process_func, *args, **kwargs)
    return re.sub(markup_re, process, phrase)


def _process_unmarked_phrase(phrase, process_func, *args, **kwargs):
    """
    Обработать фразу. В фразе не обрабатываются куски, заключенные
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
    return _process_unmarked_phrase(text_type(phrase), default_morph.inflect_ru, text_type(form))

@register.filter
def inflect_marked(phrase, form):
    if not phrase:
        return phrase
    return _process_marked_phrase(text_type(phrase), default_morph.inflect_ru, text_type(form))

@register.filter
def plural(phrase, amount):
    if not phrase:
        return phrase
    return _process_unmarked_phrase(phrase, default_morph.pluralize_inflected_ru, amount)
