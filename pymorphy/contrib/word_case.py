# -*- coding: utf-8 -*-
from __future__ import absolute_import

def restore_word_case(word, original_word):
    """
    Восстанавливает регистр слова (расположение строчных-заглавных букв).

    * word - слово, у которого требуется восстановить
      регистр (в любом регистре);
    * original_word - исходное слово (в исходном регистре);

    Пример:

    >>> from pymorphy.contrib.word_case import restore_word_case
    >>> print restore_word_case(u'ЛЮДИ', u'Человек')
    Люди

    Если сопоставить регистр слов не удается, то результат возвращается
    в нижнем регистре.
    """
    if '-' in original_word:
        parts = zip(word.split('-'), original_word.split('-'))
        return '-'.join(restore_word_case(*p) for p in parts)

    if original_word.isupper():
        return word.upper()
    elif original_word.islower():
        return word.lower()
    elif original_word.istitle():
        return word.title()
    else:
        return word.lower()

# TODO: декоратор?