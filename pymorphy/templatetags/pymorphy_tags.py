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


@register.tag(name='inflect')
def do_inflect(parser, token):
    """
    Analizes Russian and English morphology and converts phrases to the
    specified forms.

    Обертка вокруг функции django_utils.inplace.

    Позволяет указывать форму слова прямо в тексте, в том числе внутри боков
    trans/blocktrans. Таким образом информация о форме слова отправляется
    в файл переводов, где ее можно изменять, не касаясь шаблонов.
    Например, фразу "покупайте [[рыбу|вн]]" можно безболезненно заменить на
    "не уходите без [[рыбы|рд]]".

    В других языках можно просто не использовать маркер "двойные скобки",
    чтобы не обрабатывать фразу.

    Пример использования в шаблоне:
        {% blockinflate %}
            {% blocktrans %}
                Buy the {{ product_name }}
            {% endblocktrans %}
        {% endblockinflate %}

    Пример использования в файле переводов:

        msgid "Buy the %(product_name)s"
        msgstr "Не уходите без [[%(product_name)s|рд]]"

    См. также саму функцию.
    """
    nodelist = parser.parse(('endinflect',))
    parser.delete_first_token()
    return InflectNode(nodelist)

class InflectNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        output = inflect_inplace(output)
        return output

