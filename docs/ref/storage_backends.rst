Key-value - бэкенды
-------------------

.. note::

    Этот раздел справки сгенерирован автоматически.

Ниже описаны скорее детали реализации. Чтоб использовать pymorphy, их знать
необязательно.

Если вы не планируете участвовать в разработке pymorphy, полезнее ознакомиться
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



Интерфейс к CDB
"""""""""""""""

.. automodule:: pymorphy.backends.shelve_source.tinycdb_shelve
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

