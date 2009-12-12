#coding: utf-8

import re
from django import template

from pymorphy.django_conf import default_morph

register = template.Library()
word_split_re = re.compile('[\W+-]',re.U)

def _restore_register(morphed_word, word):
    """ Восстановить регистр слова """
    if word.isupper():
        return morphed_word.upper()
    elif word[0].isupper():
        return morphed_word[0].upper() + morphed_word[1:].lower()
    else:
        return morphed_word.lower()

def _process_phrase(phrase, process_func, *args, **kwargs):
    """ обработать фразу """
    words = [word for word in word_split_re.split(phrase) if word]
    result=""
    try:
        for word in words:
            processed = process_func(word.upper(), *args, **kwargs)
            processed = _restore_register(processed, word) if processed else word
            result = " ".join((result, processed))
    except:
        return phrase
    return result.lstrip()


@register.filter
def inflect(phrase, form):
    return _process_phrase(phrase, default_morph.inflect_ru, form)

@register.filter
def plural(phrase, amount):
    return _process_phrase(phrase, default_morph.pluralize_inflected_ru, amount)
