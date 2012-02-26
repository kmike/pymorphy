Использование
-------------

.. py:currentmodule:: pymorphy._morph

Подготовка
^^^^^^^^^^

Чтобы использовать морфологический анализатор, нужно сначала создать объект
класса :class:`pymorphy.Morph <Morph>`::

    from pymorphy import get_morph
    morph = get_morph('dicts/ru', 'sqlite')

Аргументы :meth:`pymorphy.get_morph <get_morph>`:

* ``path`` - обязательный параметр, путь до папки с файлами;
* ``backend`` - используемое key-value хранилище ('sqlite' или 'cdb');
* ``cached`` - использовать ли кэш (True по умолчанию).

Можно также передавать любые дополнительные аргументы, которые принимает
конструктор класса :class:`pymorphy.Morph <Morph>`.

Вместо явной передачи параметров ``path`` и ``backend`` можно использовать
переменные окружения ``PYMORPHY_DICTIONARY_PATH`` и ``PYMORPHY_DICTIONARY_BACKEND``,
например (в shell):

.. code-block:: bash

    $ export PYMORPHY_DICTIONARY_PATH = /usr/share/dicts/ru
    $ export PYMORPHY_DICTIONARY_BACKEND = cdb

и потом::

    from pymorphy import get_morph
    morph = get_morph()

.. note::

    Обратите внимание, все методы Morph ожидают, что строковые
    аргументы (в.т.ч. пустые или латинские, если используется pymorphy-speedups)
    - это unicode-строки. Кроме того, слова для обработки должны быть в верхнем
    регистре.

.. _resource-warning:
.. warning::

    Всегда старайтесь использовать единственный экземпляр анализатора.

    Объекты класса :class:`pymorphy.Morph <Morph>` требуют довольно много
    ресурсов для создания, не уничтожаются сборщиком мусора и не закрывают
    за собой файловые дескрипторы, поэтому постоянное создание
    анализаторов будет приводить к утечке ресурсов.


Получение информации о слове
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    >>> word = u'Вася'.upper()
    >>> info = morph.get_graminfo(word)[0]
    >>> print info['norm']
    ВАСЯ
    >>> print info['class']
    С
    >>> print info['info']
    мр,имя,ед,им
    >>> print info['method']
    lemma(ВАС).suffix(Я)

:meth:`Morph.get_graminfo` возвращает list всех возможных вариантов разбора
слова. Каждый вариант разбора - dict, в котором есть нормальная форма, часть
речи, грамматическая информация и служебные данные для отладки. См. также
:doc:`/ref/gram_info_ru`.


Получение нормальных форм
^^^^^^^^^^^^^^^^^^^^^^^^^

    >>> morph.normalize(u'БУТЯВКАМ')
    set(u'БУТЯВКА')

:meth:`Morph.normalize` возвращает множество (set) всех возможных нормальных
форм слова.

Склонение
^^^^^^^^^

    >>> morph.inflect_ru(u'БУТЯВКА', u'дт,мн')
    БУТЯВКАМ

:meth:`Morph.inflect_ru` возвращает слово в форме, которая соответствует
переданной и меньше всего отличается от исходной. В случае, если такую форму
найти не удается, возвращается исходное слово.

.. note::

    Этот метод на данный момент не работает с фамилиями.
    См. :ref:`names-inflection`.

См. также: :doc:`/ref/gram_info_ru`


Постановка во множественное число
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Простое::

    >>> morph.pluralize_ru(u'БУТЯВКЕ')
    БУТЯВКАМ

Согласованное с цифрой::

    >>> morph.pluralize_inflected_ru(u'ПОПУГАЙ', 1)
    ПОПУГАЙ
    >>> morph.pluralize_inflected_ru(u'ПОПУГАЙ', 2)
    ПОПУГАЯ
    >>> morph.pluralize_inflected_ru(u'ПОПУГАЙ', 38)
    ПОПУГАЕВ

См. :meth:`Morph.pluralize_ru`, :meth:`Morph.pluralize_inflected_ru`.

.. _django-integration:

