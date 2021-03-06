
.. _parameter-format:

Обозначения для грамматической информации в pymorphy
----------------------------------------------------

Реализовано 2 формата выдачи результатов: формат по умолчанию и упрощенный
стандартизованный формат, согласованный на конференции ДИАЛОГ-2010.

Полный формат
^^^^^^^^^^^^^

Это формат по умолчанию.

Обозначения соответствуют тем, что описаны тут:
http://www.aot.ru/docs/rusmorph.html

При указании в качстве параметров к методам их следует указывать через
запятую без пробелов, порядок - произвольный, регистр учитывается::

    "им,мр"

Часть речи обычно идет отдельным параметром и не передается в строках с грам.
информацией.

.. _Russian-cases:

Краткая справка по падежам
##########################

:им: Именительный (Кто? Что?)
:рд: Родительный (Кого? Чего?)
:дт: Дательный (Кому? Чему?)
:вн: Винительный (Кого? Что?)
:тв: Творительный (Кем? Чем?)
:пр: Предложный (О ком? О чём? и т.п.)
:зв: Звательный (Его формы используются при обращении к человеку - им. падеж: Аня — звательный: Ань!)


Все используемые граммемы
#########################

:мр, жр, ср: мужской, женский, средний род
:од, но: одушевленность, неодушевленность
:ед, мн: единственное, множественное число
:им, рд, дт, вн, тв, пр, зв: падежи (см. :ref:`информацию по падежам<Russian-cases>`)
:2: обозначает второй родительный или второй предложный падежи
:св, нс: совершенный, несовершенный вид
:пе, нп: переходный, непереходный глагол
:дст, стр: действительный, страдательный залог
:нст, прш, буд: настоящее, прошедшее, будущее время
:пвл: повелительная форма глагола
:1л, 2л, 3л: первое, второе, третье лицо
:0: неизменяемое
:кр: краткость (для прилагательных и причастий)
:сравн: сравнительная форма (для прилагательных)
:имя, фам, отч: имя, фамилия, отчество
:лок, орг: локативность, организация
:кач: качественное прилагательное
:вопр,относ: вопросительность и относительность (для наречий)
:дфст: слово обычно не имеет множественного числа
:опч: частая опечатка или ошибка
:жарг, арх, проф: жаргонизм, архаизм, профессионализм
:аббр: аббревиатура
:безл: безличный глагол


Части речи
##########

==============    =================   ==================
Части речи        Пример              Расшифровка
==============    =================   ==================
C                 мама                существительное
П                 красный             прилагательное
МС                он                  местоимение-существительное
Г                 идет                глагол в личной форме
ПРИЧАСТИЕ         идущий              причастие
ДЕЕПРИЧАСТИЕ      идя                 деепричастие
ИНФИНИТИВ         идти                инфинитив
МС-ПРЕДК          нечего              местоимение-предикатив
МС-П              всякий              местоименное прилагательное
ЧИСЛ              восемь              числительное (количественное)
ЧИСЛ-П            восьмой             порядковое числительное
Н                 круто               наречие
ПРЕДК             интересно           предикатив
ПРЕДЛ             под                 предлог
СОЮЗ              и                   союз
МЕЖД              ой                  междометие
ЧАСТ              же, бы              частица
ВВОДН             конечно             вводное слово
КР_ПРИЛ           красива             краткое прилагательное
КР_ПРИЧАСТИЕ      построена           краткое причастие
ПОСЛ                                  пословица
ФРАЗ
==============    =================   ==================

Упрощенный формат
^^^^^^^^^^^^^^^^^

Данные в этом формате возвращает функция get_graminfo, вызванная с параметром
standard=True. Формат был согласован на конференции Диалог-2010.

.. note::

    Получение результатов в этом формате НЕ быстрее, чем в полном.
    Разбор "внутри" все равно идет в "полном" формате,
    и лишь перед выводом данные преобразуются в упрощенный.

Части речи
##########

Для разметки используется упрощенная система частей речи:

:S: существительное (яблоня, лошадь, корпус, вечность)
:A: прилагательное (коричневый, таинственный, морской)
:V: глагол (пользоваться, обрабатывать)
:PR: предлог (под, напротив)
:CONJ: союз (и, чтобы)
:ADV: — прочие не няемые слова (частицы, междометия, вводные слова)

Могут быть размечены любым образом:

:Местоимения: (включая наречные и предикативные)
:Числительные:

Морфология (грамматические_признаки)
####################################

В категориях ADV,PR,CONJ поле остается пустым. Морфология указывается
только для S,A,V.

Здесь также используется сокращенный набор признаков:

:род: m, f, n
:падеж: nom, gen, dat, acc, ins, loc
:число: sg, pl
:время/наклонение/причастие/деепричастие: pres, past, imper, inf, partcp, ger
:залог: act, pass
:лицо: 1p, 2p, 3p
