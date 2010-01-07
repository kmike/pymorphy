API-документация
================

Морфологический анализатор
--------------------------

.. automodule:: pymorphy.morph

    .. autofunction:: get_morph

    .. autofunction:: setup_psyco

    .. autoclass:: Morph
        :members:
        :undoc-members:

        .. automethod:: __init__

    .. autoclass:: GramForm
        :members:
        :undoc-members:

Key-value - бэкенды
-------------------

Ниже описаны скорее детали реализации. Чтоб использовать pymorphy, их знать
необязательно.

Если Вы не планируете участвовать в разработке pymorphy, полезнее ознакомиться
со следующим документом: :doc:`storages`

.. automodule:: pymorphy.backends
    :members:
    :undoc-members:
    :show-inheritance:

Базовый класс
^^^^^^^^^^^^^

.. automodule:: pymorphy.backends.base
    :members:
    :undoc-members:
    :show-inheritance:


DB-источники данных
^^^^^^^^^^^^^^^^^^^

.. automodule:: pymorphy.backends.shelve_source
    :members:
    :undoc-members:
    :show-inheritance:


Интерфейс к SQLite
"""""""""""""""""""""""""""""""""""""

.. automodule:: pymorphy.backends.shelve_source.sqlite_shelve
    :members:
    :undoc-members:
    :show-inheritance:


Интерфейс к Shelve (BSDDB, GDBM, DBM)
"""""""""""""""""""""""""""""""""""""

.. automodule:: pymorphy.backends.shelve_source.shelf_with_hooks
    :members:
    :undoc-members:
    :show-inheritance:


Интерфейс к CDB
"""""""""""""""

.. automodule:: pymorphy.backends.shelve_source.cdb_shelve
    :members:
    :undoc-members:
    :show-inheritance:


Интерфейс к Tokyo Cabinet
"""""""""""""""""""""""""
.. automodule:: pymorphy.backends.shelve_source.pytc_shelve
    :members:
    :undoc-members:
    :show-inheritance:


Бэкенд для разбора исходных MRD-файлов
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Алгоритм работы с ним "как есть" должен быть совсем не таким,
как в pymorphy, pymorphy с исходными MRD-файлами работает крайне неэффективно.

Этот бэкенд используется только для переконвертации исходных словарей.

.. automodule:: pymorphy.backends.mrd_source
    :members:
    :undoc-members:
    :show-inheritance:


Pickle-источник данных
^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pymorphy.backends.pickle_source
    :members:
    :undoc-members:
    :show-inheritance:

