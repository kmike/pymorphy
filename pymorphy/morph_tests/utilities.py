#coding: utf-8
from __future__ import absolute_import, unicode_literals
from .dicts import morph_ru
from .base import MorphTestCase, unittest2

class TestPluraliseRu(MorphTestCase):

    def test_nouns(self):
        self.assertPlural('ГОРОД', 'ГОРОДА')
        self.assertPlural('СТАЛЬ', 'СТАЛИ')
        self.assertPlural('СТАЛЕВАРОМ', 'СТАЛЕВАРАМИ')

    def test_predictor_nouns(self):
        self.assertPlural('БУТЯВКОЙ', 'БУТЯВКАМИ')

    def test_verbs(self):
        self.assertPlural('ГУЛЯЛ', 'ГУЛЯЛИ')
        self.assertPlural('ГУЛЯЛА', 'ГУЛЯЛИ')
        self.assertPlural('РАСПРЫГИВАЕТСЯ', 'РАСПРЫГИВАЮТСЯ')

    def test_prefix(self):
        self.assertPlural('СУПЕРКОТ', 'СУПЕРКОТЫ')

    def test_predict_by_suffix(self):
        self.assertPlural('ДЕПЫРТАМЕНТ', 'ДЕПЫРТАМЕНТЫ')
        self.assertPlural('ХАБР', 'ХАБРЫ')

    def test_invalid_word(self):
        self.assertPlural('123', '123')

    def test_invalid_graminfo(self):
        self.assertPlural('НАЧАЛО', 'НАЧАЛА', gram_class='С')


class TestInflectRu(MorphTestCase):

    def test_inflect(self):
        self.assertInflected("СУСЛИК", "дт", "СУСЛИКУ")
        self.assertInflected("СУСЛИКИ", "дт", "СУСЛИКАМ")
        self.assertInflected("СУСЛИКОВ", "дт", "СУСЛИКАМ")
        self.assertInflected("СУСЛИКА", "дт", "СУСЛИКУ")
        self.assertInflected("СУСЛИК", "мн,дт", "СУСЛИКАМ")

    def test_verbs(self):
        self.assertInflected("ГУЛЯЮ", "прш", "ГУЛЯЛ")
        self.assertInflected("ГУЛЯЛ", "нст", "ГУЛЯЮ")

    def test_loc2(self):
        self.assertInflected('ЛЕС', 'пр', 'ЛЕСЕ')  # о лесе
        self.assertInflected('ЛЕС', 'пр,2', 'ЛЕСУ') # в лесу

        # о велосипеде
        self.assertInflected('ВЕЛОСИПЕД', 'пр', 'ВЕЛОСИПЕДЕ')

        # а тут второго предложного нет, в велосипеде
        self.assertInflected('ВЕЛОСИПЕД', 'пр,2', 'ВЕЛОСИПЕДЕ')

    def test_decline_bug(self):
        self.assertInflected('ОРЕЛ', 'рд', 'ОРЛА')

    def test_improper_guess(self):
        self.assertInflected('ОСТРОВА', 'дт', 'ОСТРОВАМ')

    def test_improper_guess2(self):
        self.assertInflected('КИЕВ', 'пр', 'КИЕВЕ')

class TestPluralizeInflected(MorphTestCase):

    def assertInflectedPlural(self, word, count, result, *args, **kwargs):
        morphed_word = morph_ru.pluralize_inflected_ru(word, count, *args, **kwargs)
        self.assertEqualRu(morphed_word, result)

    def test_parrots(self):
        self.assertInflectedPlural("ПОПУГАЙ", 1, "ПОПУГАЙ")
        self.assertInflectedPlural("ПОПУГАЙ", 2, "ПОПУГАЯ")
        self.assertInflectedPlural("ПОПУГАЙ", 3, "ПОПУГАЯ")
        self.assertInflectedPlural("ПОПУГАЙ", 4, "ПОПУГАЯ")
        self.assertInflectedPlural("ПОПУГАЙ", 5, "ПОПУГАЕВ")
        self.assertInflectedPlural("ПОПУГАЙ", 7, "ПОПУГАЕВ")
        self.assertInflectedPlural("ПОПУГАЙ", 9, "ПОПУГАЕВ")
        self.assertInflectedPlural("ПОПУГАЙ", 0, "ПОПУГАЕВ")
        self.assertInflectedPlural("ПОПУГАЙ", 10, "ПОПУГАЕВ")
        self.assertInflectedPlural("ПОПУГАЙ", 11, "ПОПУГАЕВ")
        self.assertInflectedPlural("ПОПУГАЙ", 12, "ПОПУГАЕВ")
        self.assertInflectedPlural("ПОПУГАЙ", 15, "ПОПУГАЕВ")
        self.assertInflectedPlural("ПОПУГАЙ", 19, "ПОПУГАЕВ")
        self.assertInflectedPlural("ПОПУГАЙ", 21, "ПОПУГАЙ")
        self.assertInflectedPlural("ПОПУГАЙ", 32, "ПОПУГАЯ")
        self.assertInflectedPlural("ПОПУГАЙ", 38, "ПОПУГАЕВ")
        self.assertInflectedPlural("ПОПУГАЙ", 232, "ПОПУГАЯ")
        self.assertInflectedPlural("ПОПУГАЙ", 111, "ПОПУГАЕВ")
        self.assertInflectedPlural("ПОПУГАЙ", 101, "ПОПУГАЙ")

    def test_butyavka(self):
        self.assertInflectedPlural("БУТЯВКА", 1, "БУТЯВКА")
        self.assertInflectedPlural("БУТЯВКА", 2, "БУТЯВКИ")
        self.assertInflectedPlural("БУТЯВКА", 5, "БУТЯВОК")

    def test_adjective(self):
        self.assertInflectedPlural('АКТИВНЫЙ', 1, 'АКТИВНЫЙ')
        self.assertInflectedPlural('АКТИВНЫЙ', 2, 'АКТИВНЫХ')
        self.assertInflectedPlural('АКТИВНЫЙ', 5, 'АКТИВНЫХ')

        self.assertInflectedPlural('АКТИВНАЯ', 1, 'АКТИВНАЯ')
        self.assertInflectedPlural('АКТИВНАЯ', 2, 'АКТИВНЫХ')
        self.assertInflectedPlural('АКТИВНАЯ', 5, 'АКТИВНЫХ')

    def test_gerund(self):
        self.assertInflectedPlural('ИДУЩИЙ', 1, 'ИДУЩИЙ')
        self.assertInflectedPlural('ИДУЩИЙ', 2, 'ИДУЩИХ')
        self.assertInflectedPlural('ИДУЩИЙ', 5, 'ИДУЩИХ')


if __name__ == '__main__':
    unittest2.main()
