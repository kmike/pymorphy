API-документация
================

Морфологический анализатор
--------------------------

.. automodule:: pymorphy
    :members:
    :undoc-members:

.. automodule:: pymorphy.morph
    :members:
    :undoc-members:


Key-value - бэкенды
-------------------

.. automodule:: pymorphy.backends
    :members:
    :undoc-members:

Базовый класс
^^^^^^^^^^^^^

.. automodule:: pymorphy.backends.base
    :members:
    :undoc-members:

Бэкенд для разбора исходных MRD-файлов
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Алгоритм работы с ним "как есть" должен быть совсем не таким,
как в pymorphy, pymorphy с исходными MRD-файлами работает крайне неэффективно.

Этот бэкенд используется только для переконвертации исходных словарей.

.. automodule:: pymorphy.backends.mrd_source
    :members:
    :undoc-members:


Pickle-источник данных
^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pymorphy.backends.pickle_source
    :members:
    :undoc-members:


DB-источники данных
^^^^^^^^^^^^^^^^^^^

.. automodule:: pymorphy.backends.shelve_source
    :members:
    :undoc-members:

Интерфейс к Shelve (BSDDB, GDBM, DBM)
"""""""""""""""""""""""""""""""""""""

.. automodule:: pymorphy.backends.shelve_source.shelf_with_hooks
    :members:
    :undoc-members:


Интерфейс к CDB
"""""""""""""""

.. automodule:: pymorphy.backends.shelve_source.cdb_shelve
    :members:
    :undoc-members:


Интерфейс к Tokyo Cabinet
"""""""""""""""""""""""""
.. automodule:: pymorphy.backends.shelve_source.pytc_shelve
    :members:
    :undoc-members:
