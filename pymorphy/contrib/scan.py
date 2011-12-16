#coding: utf-8
from __future__ import unicode_literals

def get_graminfo_scan(morph, word, standard=False):
    ''' Вернуть грам. информацию, считая, что текст - после сканирования. '''

    # Сначала пытаемся найти слово по словарю, без предсказателя,
    # пробуя различные характерные для отсканированных документов замены.

    gram = []
    word = word.replace('0', 'О')  # заменяем всегда
    forms = morph.get_graminfo(word, standard, False, predict_hyphenated=False)
    if forms:
        return forms

    replaces = [('4', 'А'), ('Ф', 'О'), ('J', 'А'), ('Ы', 'А')]
    # сначала пробуем найти все в словаре после замен
    for bad, good in replaces:
        if bad in word:
            forms = morph.get_graminfo(word.replace(bad, good), standard, False, predict_hyphenated=False)
            gram.extend(forms)
    if gram:
        return gram
    # если найти не удалось, то пробуем уже эвристику
    for bad, good in replaces:
        if bad in word:
            forms = morph.get_graminfo(word.replace(bad, good), standard, False, predict_hyphenated=True)
            gram.extend(forms)
    if gram:
        return gram
    # если это не помогло, включаем предсказатель и ищем по старинке
    return morph.get_graminfo(word, standard)

