#coding: utf-8
import re
from django import template
from django.utils.encoding import force_unicode

from pymorphy.django_conf import default_morph, MARKER_OPEN, MARKER_CLOSE
from pymorphy.contrib import tokenizers

register = template.Library()

markup_re = re.compile('(%s.+?%s)' % (MARKER_OPEN, MARKER_CLOSE), re.U)


def inflect(text):
    """
    Analizes Russian and English morphology and converts phrases to the
    specified forms.

    Обработывает фразы в тексте по данным, заключенным в сам текст.

    Полезно для проектов с интернационализацией, т.к. позволяет не отрывать
    описание формы слов от контекста. Например, фразу "покупайте [[рыбу|вн]]"
    можно безболезненно заменить на "не уходите без [[рыбы|рд]]" прямо в файле
    переводов, и при этом не придется менять исходный код программы, чтобы
    изменить форму слова. Также программный код не придется насаждать
    русскими словоформами вида дт,мн и тд, непонятными для нерусских
    программистов, столкнувшихся с кодом. ;)

    Пример использования в файле переводов:

        msgid "Buy the %(product_name)s"
        msgstr "Не уходите без [[%(product_name)s|рд]]"

    В других языках можно просто не использовать маркер "двойные скобки",
    чтобы не обрабатывать фразу.

    См. также блочный тег {% inflate %} для шаблонов, дающий возможность
    обернуть любой текст в эту функцию, в том числе и теги trans/blocktrans.
    Это опять таки позволяет отправить информацию о форме слова в файл
    переводов, и изменять ее там же, не касаясь шаблонов.
    """
    if not text:
        return text
    return _process_marked_inplace_phrase(force_unicode(text),
                                          default_morph.inflect_ru)


def _process_marked_inplace_phrase(text, process_func, *args, **kwargs):
    """
    Обработать фразу. В фразе обрабатываются только куски, заключенные
    в двойные квадратные скобки. Информация о форме берется из текста после
    последней разделительной вертикальной черты
    (например, "[[лошадь|рд]] Пржевальского").
    """
    def process(m):
        parts = m.group(1)[2:-2].rsplit('|', 1)
        if len(parts) == 1:
            return m.group(1)
        return _process_phrase(parts[0], process_func, parts[1],
                               *args, **kwargs)
    return re.sub(markup_re, process, text)


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
    words = tokenizers.extract_tokens(phrase)
    result=""
    try:
        for word in words:
            if tokenizers.GROUPING_SPACE_REGEX.match(word):
                result += word
                continue
            processed = process_func(word.upper(), *args, **kwargs)
            processed = _restore_register(processed, word) if processed else word
            result += processed
    except Exception:
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


