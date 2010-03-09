#coding: utf-8

from pymorphy.constants import *
from pymorphy.backends import PickleDataSource, ShelveDataSource

from utils import mprint


def _get_split_variants(word):
    """ Вернуть все варианты разбиения слова на 2 части """
    l = len(word)
    vars = [(word[0:i], word[i:l]) for i in range(1,l)]
    vars.append((word,'',))
    return vars

def _array_match(arr, filter):
    ''' Возврящает True, если все элементы из списка filter
        присутствуют в attrs
    '''
    for item in filter:
        if item and item not in arr:
            return False
    return True


def _convert_to_standard(gram_class, form_str):
    ''' Для грам. информации, полученной от метода get_gram_info и аналогичных,
        вернуть стандартное представление: (class, form)  '''
    gram_form = GramForm(form_str)

    if gram_class in [u'ПРИЧАСТИЕ', u'КР_ПРИЧАСТИЕ']:
        gram_form.form.add('partcp')
    else:
        gram_form.clear_voice()

    if gram_class == u'ИНФИНИТИВ':
        gram_form.form.add('inf')
    if gram_class == u'ДЕЕПРИЧАСТИЕ':
        gram_form.form.add('ger')

    new_form = [RU_GRAMINFO_STANDARD[attr] for attr in gram_form.form if attr in RU_GRAMINFO_STANDARD]
    return RU_CLASSES_STANDARD[gram_class], ','.join(new_form)


class GramForm(object):
    """ Класс для работы с грамматической формой """

    def __init__(self, form_string):
        self.form, self.denied_form = self.parse_str(form_string)

    @staticmethod
    def parse_str(form_string):
        splitted = form_string.split(',')
        form = [a for a in splitted if a and a[0]!='!']
        denied_form = [a[1:] for a in splitted if a and a[0]=='!']
        return set(form), set(denied_form)

    def get_form_string(self):
        return u",".join(self.form)

    def clear_number(self):
        ''' убрать информацию о числе '''
        self.form.difference_update(RU_NUMBERS)

    def clear_case(self):
        ''' убрать информацию о падеже '''
        self.form.difference_update(RU_CASES)

    def clear_gender(self):
        ''' убрать информацию о роде '''
        self.form.difference_update(RU_GENDERS)

    def clear_person(self):
        ''' убрать информацию о лице '''
        self.form.difference_update(RU_PERSONS)

    def clear_tense(self):
        ''' убрать информацию о времени '''
        self.form.difference_update(RU_TENSES)

    def clear_voice(self):
        ''' убрать информацию о залоге '''
        self.form.difference_update(RU_VOICES)

    def update(self, form_string):
        """ Обновляет параметры, по возможности оставляя все, что можно. """
        requested_form = [a for a in form_string.split(',') if a and a[0]!='!']

        for item in requested_form:

            if item in RU_NUMBERS:
                self.clear_number()
                if item==u'мн':
                    self.clear_gender()

            if item in RU_CASES:
                self.clear_case()

            if item in RU_GENDERS:
                self.clear_gender()

            if item in RU_TENSES:
                self.clear_tense()
                if item != u"нст":
                    self.clear_person()
                if item != u"прш":
                    self.clear_gender()

            if item in RU_PERSONS:
                self.clear_person()

            if item in RU_VOICES:
                self.clear_voice()

        self.form.update(requested_form)
        return self

    def match(self, gram_form):
        if not self.form.issuperset(gram_form.form): # не все параметры из gram_form есть тут
            return False
        if self.form.intersection(gram_form.denied_form):
            return False
        return True


class Morph:
    """ Класс, реализующий морфологический анализ на основе словарей из
        data_source
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
        """ Вернуть грамматическую информацию о слове и его нормальную форму.
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
                info['norm'] = ''.join(info['prefixes']) + info['norm']

        # преобразуем к стандартному виду, если требуется
        if standard:
            new_forms = []
            for form in forms:
                cls, info = _convert_to_standard(form['class'], form['info'])
                new_forms.append({'class': cls, 'info': info, 'norm': form['norm']})
            return new_forms
        return forms


    def get_graminfo_scan(self, word, standard=False):
        ''' Вернуть грам. информацию, считая, что текст - после сканирования. '''

        # Сначала пытаемся найти слово по словарю, без предсказателя,
        # пробуя различные характерные для отсканированных документов замены.

        word = word.replace(u'0', u'О')  # заменяем всегда
        forms = self.get_graminfo(word, standard, False)
        if forms:
            return forms
        replaces = [(u'4', u'А'), (u'Ф', u'О'), (u'J', u'А'), (u'Ы', u'А')]
        for bad, good in replaces:
            if bad in word:
                forms = self.get_graminfo(word.replace(bad, good), standard, False)
                if forms:
                    return forms
        # если это не помогло, включаем предсказатель и ищем по старинке
        return self.get_graminfo(word, standard)


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
        return variants

    def inflect_ru(self, word, gram_form, gram_class=None):
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
        """
        forms = self.get_graminfo(word)
        if gram_class is not None:
            forms = [form for form in forms if form['class'] == gram_class]
        if not forms:
            return word

        # FIXME: первая форма в списке не обязательно самая лучшая
        # например, лучше брать "им,мн". вместо "ед,рд".
        graminfo = forms[0]

        form = GramForm(graminfo['info'])
        form.update(gram_form)

        variants = self.decline(word, form.get_form_string(), graminfo['class'])
        if len(variants):
            return variants[0]['word']
        else:
            return word

    def pluralize_ru(self, word, gram_form='', gram_class=None):
        """
        Вернуть слово во множественном числе.
        """
        form = GramForm(gram_form).update(u'мн')
        return self.inflect_ru(word, form.get_form_string(), gram_class)

    def pluralize_inflected_ru(self, word, num, gram_class=None):
        """
        Вернуть слово в форме, которая будет сочетаться с переданным числом.
        Например: 1 попугай, 2 попугая, 5 попугаев.

        Аналог choose_plural из pytils, для которого требуется только 1
        начальная форма слова.
        """

        if num % 100 == 11: # заканчивается на 11
            form = u"мн,рд"
        elif num % 10 == 1: # заканчивается на 1
            form = u"ед,им"
        elif 11 < num % 100 < 20: # заканчивается на 12..19
            form = u'мн,рд'
        elif 2 <= num % 10 <= 4: # заканчивается на 2,3 или 4
            form = u'ед,рд'
        else:                   # заканчивается на 5..9 или 0
            form = u'мн,рд'

        return self.inflect_ru(word, form, gram_class)

    def normalize(self, word):
        """ Вернуть список нормальных форм слова """
        forms = self.get_graminfo(word)
        if not forms:
            return word
        return set(form['norm'] for form in forms)

#----------- internal methods -------------

    def _drop_cache(self):
        """ Освободить память, выделенную под внутренний кэш """
        self.data.lemmas.cache = {}
        self.data.rules.cache = {}
        self.data.endings.cache = {}


    def _decline(self, src_word):
        """ Просклонять: вернуть все грам. формы с информацией про них """

        word_graminfo = self.get_graminfo(src_word)
        forms = []

        # убираем дубликаты парадигм и варианты, для которых анализатор не
        # определил парадигму
        variants = dict([(form['paradigm_id'], form) for form in word_graminfo if 'paradigm_id' in form])

        # перебираем все возможные парадигмы и правила в них,
        # составляем варианты слов и возвращаем их
        for paradigm_id in variants:
            base_form = variants[paradigm_id]
            lemma = base_form['lemma']

            pre_prefix = ''.join(base_form.get('prefixes', []))

            paradigm = self.data.rules[paradigm_id]

            for rule in paradigm:
                suffix, ancode, prefix = rule
                cls, info, _letter  = self.data.gramtab[ancode]

                word = pre_prefix + prefix + lemma + suffix
                forms.append({
                    'word': word,
                    'class': cls,
                    'info': info,
                    'lemma': lemma,
                })
        return forms


    def _get_lemma_graminfo(self, lemma, suffix, require_prefix, method_format_str):
        """ Получить грам. информацию по лемме и суффиксу. Для леммы перебираем все
            правила, смотрим, есть ли среди них такие, которые приводят к
            образованию слов с подходящими окончаниями.
        """
        data_source = self.data
        lemma_paradigms = data_source.lemmas[lemma or '#']
        gram = []
        # для леммы смотрим все доступные парадигмы
        for paradigm_id in lemma_paradigms:
            paradigm = data_source.rules[paradigm_id]

            norm_form = lemma + paradigm[0][0]

            # все правила в парадигме
            for rule in paradigm:
                rule_suffix, rule_ancode, rule_prefix = rule
                # если по правилу выходит, что окончание такое, как надо,
                # то значит нашли, что искали
                if rule_suffix==suffix and rule_prefix==require_prefix:
                    graminfo = data_source.gramtab[rule_ancode]
                    data = {
                        'norm': norm_form,
                        'class': graminfo[0],
                        'info': graminfo[1],
                        'paradigm_id': paradigm_id,
                        'ancode': rule_ancode,
                        'lemma': lemma,
                        'method': method_format_str % (lemma, suffix)
                    }
                    # не допускаем дубликатов
                    if not data in gram:
                        gram.append(data)
        return gram


    def _flexion_graminfo(self, word, require_prefix):
        """ Вернуть грам. информацию для слова, предполагая, что все
            слово - это окончание, а основа пустая. Например, ЧЕЛОВЕК - ЛЮДИ.
            У таких слов в словарях основа записывается как "#".
        """
        return [info for info in self._get_lemma_graminfo('', word, require_prefix, '%snobase(%s)')]

    def _do_predict_by_suffix(self, word):
        """ Предсказать грамматическую форму и парадигму неизвестного слова
            по последним 5 буквам.
        """
        data_source = self.data

        gram=[]
        for i in (5,4,3,2,1):
            end = word[-i:]
            if end in data_source.endings:

                # парадигмы, по которым могут образовываться слова с таким
                # завершением
                paradigms = data_source.endings[end]

                for paradigm_id in paradigms:

                    # номера возможных правил
                    rules_id_list = paradigms[paradigm_id]
                    # lookup-словарь для правил
                    rules_list = data_source.rules[paradigm_id]

                    # для всех правил определяем часть речи, если она
                    # продуктивная, то добавляем вариант слова
                    for id in rules_id_list:
                        rule = rules_list[id]
                        suffix, ancode = rule[0], rule[1]
                        graminfo = data_source.gramtab[ancode]
                        if graminfo[0] in PRODUCTIVE_CLASSES:
                            # норм. форма слова получается заменой суффикса
                            # на суффикс начальной формы
                            suffix_len = len(suffix)
                            predicted_lemma = word[0:-suffix_len] if suffix_len else word
                            norm_form = predicted_lemma + rules_list[0][0]
                            gram.append({
                                         'norm': norm_form,
                                         'class':graminfo[0],
                                         'info': graminfo[1],
                                         'paradigm_id': paradigm_id,
                                         'ancode': ancode,
                                         'lemma': predicted_lemma,
                                         'method': 'predict(...%s)' % end
                                       })

                # нашли хотя бы одно окончание слова данной длины, больше не ищем
                if gram:
                    break
        return gram


    def _static_prefix_graminfo(self, variants, require_prefix=''):
        """ Определить грамматическую форму слова, пробуя отбросить
            фиксированные префиксы. В функцию передается уже подготовленный
            список вариантов разбиения слова.
        """
        gram = []
        if not self.check_prefixes:
            return gram

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


    def _predict_by_prefix_graminfo(self, word, require_prefix):
        """ Предсказать грамматическую форму неизвестного слова по
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
        split_indexes = range(1, 1+min(self.prediction_max_prefix_len,
                                       len(word)-self.prediction_min_suffix_len))
        variants = [(word[:i], word[i:]) for i in split_indexes]
        for (prefix, suffix) in variants:
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
        ''' Обработка буквы Ё. Пробуем проверить, не получится ли определить
            данные слова, если в нем Е заменить на Ё. Если получилось,
            результат возвращаем все-таки с Е.

            Буквы Ё на Е в словарях можно заменить на этапе кодирования
            словарей (это поведение по умолчанию). Все равно в словарях
            поддержка Ё не до конца полная.
        '''
        gram = self._get_graminfo(word.replace(u'Е', u'Ё'), require_prefix,
                                  predict_EE = False)
        for info in gram:
            info['method'] = info['method'].replace(u'Ё', u'Е')
        return gram


    def _get_graminfo(self, word, require_prefix='', predict = True, predict_EE = True):
        """ Получить грам. информацию о слове.
            Внутренний вариант для поддержки рекурсии с возможностью временно
            отключать предсказатель и возможностью требовать наличие
            определенного префикса у результата.
        """
        gram = []

        # вариант с пустой основой слова
        gram.extend(self._flexion_graminfo(word, require_prefix))

        # основная проверка по словарю: разбиваем слово на 2 части,
        # считаем одну из них основой, другую окончанием
        # (префикс считаем пустым, его обработаем отдельно)
        variants = _get_split_variants(word)
        for (lemma, suffix) in variants:
            if lemma in self.data.lemmas:
                gram.extend(
                    [info for info in
                        self._get_lemma_graminfo(lemma, suffix, require_prefix,
                                                 'lemma(%s).suffix(%s)')
                    ]
                )

        # вариант с фиксированным префиксом
        gram.extend(self._static_prefix_graminfo(variants, require_prefix))

        # обработка буквы Ё, если требуется
        if not gram and self.handle_EE and predict_EE:
            gram.extend(self._handle_EE(word, require_prefix))

        # обработка предсказания по началу слова, если требуется
        if not gram and predict and self.predict_by_prefix:
            gram.extend(self._predict_by_prefix_graminfo(word, require_prefix))

        # обработка предсказания по концу слова, если требуется
        if not gram and predict and self.predict_by_suffix:
            gram.extend(self._do_predict_by_suffix(word))

        return gram


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


def setup_psyco():
    ''' Попытаться оптимизировать узкие места с помощью psyco '''
    try:
        import psyco
        from pymorphy.backends.shelve_source.shelf_with_hooks import ShelfWithHooks
        psyco.bind(Morph._get_graminfo)
        psyco.bind(Morph._get_lemma_graminfo)
        psyco.bind(GramForm.__init__)
        psyco.bind(ShelfWithHooks._getitem__cached)
        psyco.bind(ShelfWithHooks._contains__cached)
        psyco.bind(_get_split_variants)
    except ImportError:
        pass



