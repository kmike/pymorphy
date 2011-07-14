# -*- coding: utf-8 -*-
# XXX: или все-таки лучше завязаться на nltk?

import re

SPACE_REGEX = re.compile('[^\w_-]|[+]', re.U)
GROUPING_SPACE_REGEX = re.compile('([^\w_-]|[+])', re.U)

def extract_tokens(text):
    """ Разбить текст на токены - слова, пробелы, знаки препинания. """
    return filter(None, GROUPING_SPACE_REGEX.split(text))


def extract_words(text):
    """
    Разбить текст на слова. Пунктуация игнорируется.
    Слова, пишущиеся через дефис, считаются 1 словом.
    Пример использования::

        from pymorphy.contrib import tokenizers

        for word in tokenizers.extract_words(text):
            print word

    .. note::

        возвращает генератор, а не list

    """
    for word in SPACE_REGEX.split(text):
        test_word = word.replace('-','')
        if not test_word or test_word.isspace() or test_word.isdigit():
            continue
        word = word.strip('-')
        yield word
