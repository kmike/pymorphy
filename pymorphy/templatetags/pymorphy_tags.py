#coding: utf-8
import re
from django import template

from pymorphy.django_conf import default_morph

register = template.Library()
word_split_re = re.compile('[\W+-]',re.U)

@register.filter
def inflect(phrase, form):
    words = word_split_re.split(phrase)
    result=""
    try:
        for word in words:
            if word:
                inflected_word = default_morph.inflect_ru(word.upper(), form).lower()
                if inflected_word:
                    # восстанавливаем регистр
                    if word.isupper():
                        inflected_word = inflected_word.upper()
                    elif word[0].isupper():
                        inflected_word = inflected_word[0].upper() + inflected_word[1:]
                else:
                    inflected_word = word
                result = " ".join((result, inflected_word))
    except:
        return phrase
    return result.lstrip()