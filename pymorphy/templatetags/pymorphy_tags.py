#coding: utf-8
from django import template

from pymorphy.django_conf import default_morph
from pymorphy.django_utils import inflect as inflect_inplace
from pymorphy.django_utils import _process_unmarked_phrase, _process_marked_phrase


register = template.Library()

@register.filter
def inflect(phrase, form):
    if not phrase:
        return phrase
    return _process_unmarked_phrase(unicode(phrase), default_morph.inflect_ru, unicode(form))

@register.filter
def inflect_marked(phrase, form):
    if not phrase:
        return phrase
    return _process_marked_phrase(unicode(phrase), default_morph.inflect_ru, unicode(form))

@register.filter
def plural(phrase, amount):
    if not phrase:
        return phrase
    return _process_unmarked_phrase(phrase, default_morph.pluralize_inflected_ru, amount)


@register.tag
def blockinflect(parser, token):
    """
    Analizes Russian and English morphology and converts phrases to the
    specified forms.

    Обертка вокруг функции django_utils.inflect.

    Позволяет указывать форму слова прямо в тексте, в том числе внутри боков
    trans/blocktrans. Таким образом информация о форме слова отправляется
    в файл переводов, где ее можно изменять, не касаясь шаблонов.
    Например, фразу "покупайте [[рыбу|вн]]" можно безболезненно заменить на
    "не уходите без [[рыбы|рд]]".

    В других языках можно просто не использовать маркер "двойные скобки",
    чтобы не обрабатывать фразу.

    Пример использования в шаблоне:
        {% blockinflect %}
            {% blocktrans %}
                Buy the {{ product_name }}
            {% endblocktrans %}
        {% endblockinflect %}

    Пример использования в файле переводов:

        msgid "Buy the %(product_name)s"
        msgstr "Не уходите без [[%(product_name)s|рд]]"

    См. также саму функцию.
    """
    nodelist = parser.parse(('endblockinflect',))
    parser.delete_first_token()
    return InflectNode(nodelist)


class InflectNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        output = inflect_inplace(output)
        return output


@register.tag
def blockplural(parser, token):
    """
    Same as plural filter

    Example:
        {% blockplural amount %}{% trans "Book" %}{% endblockplural %}
    """
    nodelist = parser.parse(('endblockplural',))
    parser.delete_first_token()
    tag_name, amount = token.split_contents()
    return PluralNode(nodelist, amount)


class PluralNode(template.Node):

    def __init__(self, nodelist, amount):
        self.nodelist = nodelist
        self.amount = template.Variable(amount)

    def render(self, context):
        output = self.nodelist.render(context)
        if not output:
            return output
        return _process_unmarked_phrase(
            output, default_morph.pluralize_inflected_ru,
            self.amount.resolve(context))
