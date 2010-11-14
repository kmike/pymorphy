#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management import call_command

settings.configure(
    INSTALLED_APPS=('pymorphy',),
    PYMORPHY_DICTS = {
        'ru': {
            'dir': 'dicts/converted/ru',
            'backend': 'shelve',
            'use_cache': True,
            'default': True,
        },
        'en': {
            'dir': 'dicts/converted/en',
        },
    },
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }}
)

if __name__ == "__main__":
    call_command('test', 'pymorphy')
