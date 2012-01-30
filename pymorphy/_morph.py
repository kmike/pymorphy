# coding: utf-8
## cython: profile=True
from __future__ import unicode_literals
from copy import deepcopy

from pymorphy.constants import *
from pymorphy.backends import PickleDataSource, ShelveDataSource
from pymorphy.utils import pprint, get_split_variants

def _array_match(arr, filter):
    '''
    Возвращает True, если все элементы из списка filter
    присутствуют в attrs
    '''
    for item in filter:
        if item and item not in arr:
            return False
    return True


def _convert_to_standard(gram_class, form_str):
    '''
    Для грам. информации, полученной от метода get_gram_info и аналогичных,
    вернуть стандартное представление: (class, form)
    '''
    gram_form = GramForm(form_str)

    if gram_class in ['ПРИЧАСТИЕ', 'КР_ПРИЧАСТИЕ']:
        gram_form.form.add('partcp')
    else:
        gram_form.clear_voice()

    if gram_class == 'ИНФИНИТИВ':
        gram_form.form.add('inf')
    if gram_class == 'ДЕЕПРИЧАСТИЕ':
        gram_form.form.add('ger')

    new_form = [RU_GRAMINFO_STANDARD[attr] for attr in gram_form.form if attr in RU_GRAMINFO_STANDARD]
    return RU_CLASSES_STANDARD[gram_class], ','.join(new_form)


def _parse_gram_str(form_string):
    splitted = form_string.split(',')
    form = [a for a in splitted if a and a[0]!='!']
    denied_form = [a[1:] for a in splitted if a and a[0]=='!']
    return set(form), set(denied_form)

class GramForm(object):
    """ Класс для работы с грамматической формой """

    def __init__(self, form_string):
        self.form, self.denied_form = _parse_gram_str(form_string)

    def get_form_string(self):
        return ",".join(self.form)

    def clear_number(self):
        ''' убрать информацию о числе '''
        self.form.difference_update(RU_NUMBERS)
        return self

    def clear_case(self):
        ''' убрать информацию о падеже '''
        self.form.difference_update(RU_CASES)
        return self

    def clear_gender(self):
        ''' убрать информацию о роде '''
        self.form.difference_update(RU_GENDERS)
        return self

    def clear_person(self):
        ''' убрать информацию о лице '''
        self.form.difference_update(RU_PERSONS)
        return self

    def clear_tense(self):
        ''' убрать информацию о времени '''
        self.form.difference_update(RU_TENSES)
        return self

    def clear_voice(self):
        ''' убрать информацию о залоге '''
        self.form.difference_update(RU_VOICES)
        return self

    def clear_animacy(self):
        ''' убрать информацию о одушевленности '''
        self.form.difference_update(RU_ANIMACY)

    def update(self, form_string):
        """ Обновляет параметры, по возможности оставляя все, что можно. """
        requested_form = [a for a in form_string.split(',') if a and a[0]!='!']

        for item in requested_form:

            if item in RU_NUMBERS:
                self.clear_number()
                if item=='мн':
                    self.clear_gender()

            if item in RU_CASES:
                self.clear_case()

            if item in RU_GENDERS:
                self.clear_gender()

            if item in RU_TENSES:
                self.clear_tense()
                if item != "нст":
                    self.clear_person()
                if item != "прш":
                    self.clear_gender()

            if item in RU_PERSONS:
                self.clear_person()

            if item in RU_VOICES:
                self.clear_voice()

            if item in RU_ANIMACY:
                self.clear_animacy()

        self.form.update(requested_form)
        return self

    def match(self, gram_form):
        if not self.form.issuperset(gram_form.form): # не все параметры из gram_form есть тут
            return False
        if self.form.intersection(gram_form.denied_form):
            return False
        return True

    def match_string(self, str_form):
        return str_form if self.match(GramForm(str_form)) else None


def _guess_best_form(forms):
    """ выбирает наиболее вероятную форму слова, для склонятора """
    first_guess = forms[0]

    # Для существительных первая форма в списке не обязательно самая лучшая:
    # например, обычно лучше брать "им,мн" вместо "ед,рд".
    if first_guess['class'] == 'С':
        good = GramForm('им')

        for form in forms:
            gram_form = GramForm(form['info'])
            if gram_form.match(good):
                return form, form['lemma']

    return first_guess, None


class Morph(object):
    """
    Класс, реализующий морфологический анализ на основе словарей из data_source
    """

    def __init__(self, data_source, check_prefixes = True,
                 predict_by_prefix = True, predict_by_suffix = True,
                 handle_EE = False):
        '''
        Параметры конструктора:

        * data_source: источник данных. Может быть
          :class:`ShelveDataSource`, :class:`MrdDataSource`,
          :class:`PickleDataSource` или любой другой наследник
          :class:`DictDataSource`, у которого есть атрибуты
          rules, lemmas, prefixes, gramtab, rule_freq, endings,
          possible_rule_prefixes, поддерживающие доступ по ключу.
        * check_prefixes: проверять ли вообще префиксы
        * predict_by_prefix: предсказывать ли по префиксу
        * predict_by_suffix: предсказывать ли по суффиксу
        * handle_EE: как обрабатывать букву ё. Если True, то все буквы ё
          считаются равными е, если False - разными буквами. По умолчанию
          в словарях все буквы ё заменены на е, и ожидается, что в
          пользовательском вводе букв ё не будет (handle_EE=False).
          Если словарь сконвертирован с handle_EE=True (в нем сохранены
          буквы ё), то буквы е и ё будут считаться разными буквами, это
          может привести к неожиданностям, т.к. часто вместо ё пишут е, а
          в словаре будет слово только с ё. При handle_EE=True запросы
          выполняются по 2 раза, со словом "как есть" и со словом, у
          которого все е заменены на ё.
        '''

        self.data = data_source
        self.data.load()

        self.check_prefixes = check_prefixes
        self.predict_by_prefix = predict_by_prefix
        self.predict_by_suffix = predict_by_suffix

        self.prediction_max_prefix_len = 5 #actually 5=4+1
        self.prediction_min_suffix_len = 3 #actually 3=4-1

        self.handle_EE = handle_EE

    def get_graminfo(self, word, standard=False, predict=True, **kwargs):
        """
        Вернуть грамматическую информацию о слове и его нормальную форму.
        Если параметр standard=True, то для каждого варианта разбора
        результаты возвращаются в стандартном виде (словарь вида
        {'class': <class>, 'info': <info>, 'norm': <norm>}, обозначения
        согласованы с теми, что приняты на конференции Диалог-2010. Если
        standard = False (по умолчанию), то возвращается больше информации
        (детальное разбиение на части речи, больше морфологических
        признаков, информация об использованном алгоритме),
        обозначения определяются структурой словарей.
        """
        forms = self._get_graminfo(word, predict=predict, **kwargs)
        # приписываем статичные префиксы к нормальным формам слова
        for info in forms:
            if 'prefixes' in info:
                info['norm'] = (''.join(info['prefixes']) + info['norm']).strip('-')

        # преобразуем к стандартному виду, если требуется
        if standard:
            new_forms = []
            for form in forms:
                cls, info = _convert_to_standard(form['class'], form['info'])
                new_forms.append({'class': cls, 'info': info, 'norm': form['norm']})
            return new_forms
        return forms


    def decline(self, word, gram_form='', gram_class=None):
        """
        Вернуть все варианты слова, соответствующие заданной
        грамматической форме и части речи.

        Параметры:

        * word - слово, которое хотим склонять
        * gram_form - желаемые характеристики грам. формы. Выступает в роли
          фильтра. Может быть пустым, тогда будут возвращены все
          формы слова.
        * gram_class - часть речи. Если передан этот параметр, то слово
          будет считаться словом этой части речи (если возможно), и
          склоняться будет соответственно. Если параметр не передан,
          ограничения на часть речи накладываться не будут.
        """
        requested_attrs = gram_form.split(',')
        variants = []
        for form in self._decline(word):
            if gram_class:
                if form['class'] != gram_class:
                    continue
            form_attrs = form['info'].split(',')
            if _array_match(form_attrs, requested_attrs):
                variants.append(form)

        if not variants and '2' in requested_attrs:
            return self.decline(word, gram_form.replace('2',''), gram_class)

        return variants

    def inflect_ru(self, word, gram_form, gram_class=None, smart_guess=True):
        """
        Вернуть вариант слова, который соотвествует данной грамматической
        форме и части речи, а также менее всего отличается от исходного.

        Параметры:

        * word - слово, которое хотим склонять
        * gram_form - желаемые характеристики грам. формы
        * gram_class - часть речи. Если передан этот параметр, то слово
          будет считаться словом этой части речи (если возможно), и
          склоняться будет соответственно. Требуется для устранения
          неоднозначностей.
        * smart_guess (True по умолчанию). Если smart_guess is True, то
          исходная форма слова будет угадываться как наиболее близкая к
          нормальной (для существительных будет отдано предпочтение варианту
          разбора с именительным падежом).
        """
        forms = self.get_graminfo(word)
        if gram_class is not None:
            forms = [form for form in forms if form['class'] == gram_class]
        if not forms:
            return word

        # проверка через is, чтоб можно было в будущем
        # передавать в smart_guess строки с подсказками
        if smart_guess is True:
            graminfo, lemma = _guess_best_form(forms)
        else:
            graminfo, lemma = forms[0], None

        form = GramForm(graminfo['info'])
        form.update(gram_form)

        variants = self.decline(word, form.get_form_string(), graminfo['class'])
        if len(variants):
            if lemma is not None:
                for variant in variants:
                    if variant['lemma'] == lemma:
                        return variant['word']
            return variants[0]['word']
        else:
            return word

    def pluralize_ru(self, word, gram_form='', gram_class=None):
        """
        Вернуть слово во множественном числе.
        """
        form = GramForm(gram_form).update('мн')
        return self.inflect_ru(word, form.get_form_string(), gram_class)

    def pluralize_inflected_ru(self, word, num, gram_class=None):
        """
        Вернуть слово в форме, которая будет сочетаться с переданным числом.
        Например: 1 попугай, 2 попугая, 5 попугаев.

        Аналог choose_plural из pytils, для которого требуется только 1
        начальная форма слова.
        """

        form_info = {
            'С':         ['ед,им', 'ед,рд', 'мн,рд'],
            'П':         ['ед,им', 'мн,рд', 'мн,рд'],
            'ПРИЧАСТИЕ': ['ед,им', 'мн,рд', 'мн,рд'],
            'ЧИСЛ-П':    ['ед,им', 'мн,рд', 'мн,рд'],
        }

        if (num % 10 == 1) and (num % 100 != 11):
            index = 0
        else:
            if (num % 10 >= 2) and (num % 10 <= 4) and (num % 100 < 10 or num % 100 >= 20):
                index = 1
            else:
                index = 2

        if gram_class is None:
            forms = self.get_graminfo(word)
            if not forms:
                return word
            gram_class = forms[0]['class']

        inflect_rules = form_info.get(gram_class, form_info['С'])
        return self.inflect_ru(word, inflect_rules[index], gram_class)

    def normalize(self, word):
        """ Вернуть список нормальных форм слова """
        forms = self.get_graminfo(word)
        if not forms:
            return word
        return set(form['norm'] for form in forms)

#----------- internal methods -------------

    def _decline(self, src_word):
        """ Просклонять: вернуть все грам. формы с информацией про них """

        word_graminfo = self.get_graminfo(src_word)
        forms = []

        # убираем дубликаты парадигм и варианты, для которых анализатор не
        # определил парадигму
        seen = set()
        variants = []
        for form in word_graminfo:
            if 'paradigm_id' not in form:
                continue
            paradigm_id = form['paradigm_id']
            if paradigm_id in seen:
                continue
            seen.add(paradigm_id)
            variants.append((paradigm_id, form))

        # перебираем все возможные парадигмы и правила в них,
        # составляем варианты слов и возвращаем их
        gramtab = self.data.gramtab
        rules = self.data.rules

        for paradigm_id, base_form in variants:
            lemma = base_form['lemma']
            pre_prefix = ''.join(base_form.get('prefixes', []))
            paradigm = rules[paradigm_id]
            for suffix in paradigm:
                ending = lemma + suffix
                for ancode, prefix in paradigm[suffix]:
                    cls, info, _letter  = gramtab[ancode]
                    word = pre_prefix + prefix + ending
                    forms.append({
                        'word': word,
                        'class': cls,
                        'info': info,
                        'lemma': lemma,
                    })
        return forms

    def _analyzed_word_information(self, lemma, paradigm_id, rule):
        """
        Для результата разбора возвращает словарь с подробной информацией
        """
        norm_form = self._get_normal_form(lemma, paradigm_id)

        suffix, ancode, prefix = rule
        gram_class, info, _ = self.data.gramtab[ancode]

        data = {
            'norm': norm_form,
            'class': gram_class,
            'info': info,
            'paradigm_id': paradigm_id,
            'ancode': ancode,
            'lemma': lemma,
            'method': 'lemma(%s).suffix(%s)' % (lemma, suffix)
        }
        return data

    def _get_normal_form(self, lemma, paradigm_id):
        """
        Собирает из леммы и номера парадигмы слова его нормальную форму.
        """
        suffix, ancode, prefix = self.data.normal_forms[paradigm_id]
        # XXX: а префикса тут почему нет?
        return lemma + suffix

    def _word_graminfo(self, word, require_prefix):
        """
        Возвращает результаты основного разбора слова по словарю.
        """
        for lemma, paradigm_id, rule in self.data.analyze(word):
            if rule[2] == require_prefix:
               yield self._analyzed_word_information(lemma, paradigm_id, rule)


    def _do_predict_by_suffix(self, word):
        """
        Предсказать грамматическую форму и парадигму неизвестного слова
        по последним 5 буквам.
        """
        endings = self.data.endings
        gramtab = self.data.gramtab

        gram=[]
        for i in 5,4,3,2,1:
            end = word[-i:]
            if end in endings:

                # парадигмы, по которым могут образовываться слова с таким
                # завершением
                paradigms = endings[end]

                for paradigm_id in paradigms:
                    rules = paradigms[paradigm_id]
                    for suffix, ancode, prefix in rules:

                        gram_class, info, _ = gramtab[ancode]
                        if gram_class in PRODUCTIVE_CLASSES:
                            # норм. форма слова получается заменой суффикса
                            # на суффикс начальной формы
                            suffix_len = len(suffix)
                            predicted_lemma = word[0:-suffix_len] if suffix_len else word
                            norm_form = self._get_normal_form(predicted_lemma, paradigm_id)
                            gram.append({
                                'norm': norm_form,
                                'class': gram_class,
                                'info': info,
                                'paradigm_id': paradigm_id,
                                'ancode': ancode,
                                'lemma': predicted_lemma,
                                'method': 'predict(...%s)' % end
                            })

                # нашли хотя бы одно окончание слова данной длины, больше не ищем
                if gram:
                    break

        # Если слово не было предсказано как существительное, можно добавлять
        # вариант с неизменяемым существительным. Для миллиона слов
        # сбалансированной коллекции - 1000 срабатываний, из них < 10 правильных.
        # Пока думаю, что оно того не стоит.

#        if not any([form['class'] in NOUNS for form in gram]):
#            gram.append({
#                'class': 'С',
#                'info': "ср,жр,мр,пр,тв,вн,дт,рд,им,ед,мн,",
#                'norm': word,
#                'method':'predict(IMMUTABLE)',
#            })

        return gram


    def _static_prefix_graminfo(self, word, require_prefix=''):
        """
        Определить грамматическую форму слова, пробуя отбросить
        фиксированные префиксы.
        """
        gram = []
        if not self.check_prefixes:
            return gram

        variants = get_split_variants(word)

        for (prefix, suffix) in variants:

            # один из фиксированных префиксов?
            if prefix in self.data.prefixes:
                # да, получаем рекурсивно грам. информацию про оставшуюся часть
                # слова (с отключенным предсказателем)
                base_forms = self._get_graminfo(suffix,
                                                require_prefix = require_prefix,
                                                predict = False,
                                                predict_EE = False)

                # приписываем префикс обратно к полученным нормальным формам
                for form in base_forms:
                    form['prefixes'] = [prefix] + form.get('prefixes', [])
                    form['method'] = 'prefix(%s).%s' % (prefix, form['method'])
                gram.extend(base_forms)

            # одна из возможных приставок к лемме? (ПО- и НАИ-)
            if prefix in self.data.possible_rule_prefixes:
                # добавляем информацию, отбрасывая приставку, т.к. она
                # добавляется и удаляется в зависимости от грамм. формы.
                # например, НАИСТАРЕЙШИЙ -> СТАРЫЙ
                gram.extend(self._get_graminfo(suffix,
                                               require_prefix = prefix,
                                               predict = False,
                                               predict_EE = False))
        return gram


    def _predict_hyphenated(self, word, require_prefix='', predict=True):
        """ Предсказать грамматическую форму слова, которое пишется через дефис """
        gram = []
        if not '-' in word:
            return gram

        left, right = word.split('-', 1)
        left = require_prefix+left if left else ''
        # анализируем правую часть отдельно, считая левую неизменяемой приставкой
        # Пр.: интернет-магазин, воздушно-капельный
        right_forms = self._get_graminfo(right, predict=predict)
        gram = deepcopy(right_forms)
        for form in gram:
            form['prefixes'] = [left+'-'] + form.get('prefixes', [])
            form['method'] = 'hyphen-prefix(%s).%s' % (left, form['method'])

        # Если есть варианты разбора первой части, которые совпадают с
        # вариантами разбора второй, то есть вероятность, что у нас
        # 2 равнозначные части, которые обе должны склоняться.
        # Пр.: человек-гора, команд-участниц, компания-производитель
        left_forms = self._get_graminfo(left, require_prefix = require_prefix, predict=predict)
        for left_form in left_forms:
            gram_form = GramForm(left_form['info'])
            gram_form.clear_gender()
            for right_form in right_forms:
                if right_form['class'] == left_form['class']:
                    if GramForm(right_form['info']).match(gram_form):
                        data = {
                            'norm': (require_prefix+left_form['norm'] + '-' + right_form['norm']).strip('-'),
                            'class': left_form['class'],
                            'info': left_form['info'],
                            'lemma': left_form['lemma'] + '+' + right_form['lemma'],
                            'method': "word-formation(%s + %s)" % (
                                           left_form['method'],
                                           right_form['method'],
                                       )
                        }
                        gram.append(data)
        return gram


    def _predict_by_prefix_graminfo(self, word, require_prefix):
        """
        Предсказать грамматическую форму неизвестного слова по
        префиксу. Если слова отличаются только тем, что к одному из них
        приписано что-то спереди, то, скорее всего, склоняться они будут
        однаково. Пробуем сначала одну первую букву слова считать префиксом,
        потом 2 первых буквы и т.д. А то, что осталось, передаем
        морфологическому анализатору.
        """
        gram=[]
        if not self.predict_by_prefix:
            return gram

        # все варианты разбиений с учетом ограничений на длину префикса и окончания
        max_split = min(
            self.prediction_max_prefix_len,
            len(word)-self.prediction_min_suffix_len
        )
        split_indexes = range(1, 1+max_split)
        variants = [(word[:i], word[i:]) for i in split_indexes]

        for prefix, suffix in variants:
            # оторвали префикс, смотрим, удастся ли что-то узнать
            base_forms = self._get_graminfo(suffix,
                                            require_prefix=require_prefix,
                                            predict=False,
                                            predict_EE = False)

            # убираем непродуктивные части речи
            base_forms = [form for form in base_forms
                          if form['class'] in PRODUCTIVE_CLASSES]

            # приписываем префикс обратно
            for form in base_forms:
                form['prefixes'] = [prefix] + form.get('prefixes', [])
                form['method'] = 'predict-prefix(%s).%s' % (prefix, form['method'])
            gram.extend(base_forms)
        return gram


    def _handle_EE(self, word, require_prefix):
        '''
        Обработка буквы Ё. Пробуем проверить, не получится ли определить
        данные слова, если в нем Е заменить на Ё. Если получилось,
        результат возвращаем все-таки с Е.

        Буквы Ё на Е в словарях можно заменить на этапе кодирования
        словарей (это поведение по умолчанию). Все равно в словарях
        поддержка Ё не до конца полная.
        '''
        gram = self._get_graminfo(word.replace('Е', 'Ё'), require_prefix,
                                  predict_EE = False)
        for info in gram:
            info['method'] = info['method'].replace('Ё', 'Е')
        return gram

    def _get_graminfo(self, word, require_prefix='', predict = True,
                      predict_EE = True, predict_hyphenated=True):
        """
        Получить грамматическую информацию о слове.
        Внутренний вариант для поддержки рекурсии с возможностью временно
        отключать предсказатель и возможностью требовать наличие
        определенного префикса у результата.
        """
        gram = []

        # основной разбор
        gram.extend(self._word_graminfo(word, require_prefix))

        # вариант с фиксированным префиксом
        gram.extend(self._static_prefix_graminfo(word, require_prefix))

        # обработка буквы Ё, если требуется
        if not gram and self.handle_EE and predict_EE:
            gram.extend(self._handle_EE(word, require_prefix))

        # обработка слов с дефисами
        if not gram and predict_hyphenated:
            gram.extend(self._predict_hyphenated(word, require_prefix, predict))

        # обработка предсказания по началу слова, если требуется
        if not gram and predict and self.predict_by_prefix:
            gram.extend(self._predict_by_prefix_graminfo(word, require_prefix))

        # обработка предсказания по концу слова, если требуется
        if not gram and predict and self.predict_by_suffix:
            gram.extend(self._do_predict_by_suffix(word))

        return gram

    def __str__(self):
        return 'Morph [%s]' % self.data


def get_morph(path, backend='sqlite', cached=True, **kwargs):
    """
    Вернуть объект с морфологическим анализатором (Morph).

    Параметры:

    * path - путь к папке с файлами словарей (или полное имя файла со словарем, в случае pickle)
    * backend - тип словарей. Может быть 'shelve', 'tch', 'tcb', 'cdb', 'pickle', 'sqlite'.
    * cached - кешировать ли данные в оперативной памяти

    Также можно указывать все параметры, которые принимает конструктор класса
    Morph.

    """
    if backend == 'pickle':
        return Morph(PickleDataSource(path), **kwargs)
    return Morph(ShelveDataSource(path, backend, cached=cached), **kwargs)

