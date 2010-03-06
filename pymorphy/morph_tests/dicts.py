#coding: utf-8
import os
from pymorphy.morph import get_morph

_path = os.path.join(os.path.dirname(__file__), '..', '..', 'dicts', 'converted')
DICT_PATH = os.path.abspath(_path)

morph_ru = get_morph(os.path.join(DICT_PATH, 'ru'))
morph_en = get_morph(os.path.join(DICT_PATH, 'en'))
