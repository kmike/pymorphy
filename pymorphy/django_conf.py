#coding: utf-8
"""
Минимальный пример настроек словарей в settings.py::

    PYMORPHY_DICTS = {
        'ru': { 'dir': '/usr/share/pymorphy/ru' },
    }

Более сложный пример::

    PYMORPHY_DICTS = {
        'ru': {
            'dir': '/usr/share/pymorphy/ru',
            'backend': 'tcb',
            'use_cache': True,
        },

        'en': {
            'dir': '/usr/share/pymorphy/en',
            'backend': 'shelve',
            'use_cache': True,
            'default': True
        },
    }

"""

from django.conf import settings

from django.core.exceptions import ImproperlyConfigured

from pymorphy.morph import get_morph


default_morph = None
try:
    PYMORPHY_DICTS = settings.PYMORPHY_DICTS
    morphs = {}
    for dict_name in PYMORPHY_DICTS:
        options = {'backend': 'sqlite', 'use_cache': True, 'default': False}
        options.update(PYMORPHY_DICTS[dict_name])
        morphs[dict_name] = get_morph(options['dir'], options['backend'], options['use_cache'])
        if default_morph is None or options['default']:
            default_morph = morphs[dict_name]

except AttributeError:
    raise ImproperlyConfigured('correct settings.PYMORPHY_DICTS is required for pymorphy template tags.')

MARKER_OPEN = getattr(settings, 'PYMORPHY_MARKER_OPEN', '\[\[')
MARKER_CLOSE = getattr(settings, 'PYMORPHY_MARKER_CLOSE', '\]\]')
