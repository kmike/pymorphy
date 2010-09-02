#coding: utf-8
import re

space_regex = re.compile('([^\w_-]|[+])', re.U)

def split_into_words(text):
    """ Разбить текст на слова """
    return filter(None, space_regex.split(text))

if __name__ == '__main__':
    txt = u"""Это  отразилось: на количественном,и на качествен_ном
    росте карельско-финляндского сотрудничества - офигеть! кони+лошади=масло."""
    for w in split_into_words(txt):
        print w
