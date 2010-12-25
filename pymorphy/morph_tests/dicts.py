#coding: utf-8
import os
from pymorphy.morph import get_morph

_path = os.path.join(os.path.dirname(__file__), '..', '..', 'dicts', 'converted')
DICT_PATH = os.path.abspath(_path)
RU_DICT = os.path.join(DICT_PATH, 'ru')
EN_DICT = os.path.join(DICT_PATH, 'en')

morph_ru = get_morph(RU_DICT)
morph_en = get_morph(EN_DICT)
