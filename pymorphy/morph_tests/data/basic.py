#coding: utf-8

"""
Образцы разборов для дорожки "Морфология" сделаны С.Ковалем
в соответствии с согласованным на конференции Диалог-2010 инвентарем
признаков.

В образцах на следующих листах используются три вида условных обозначений:

* знак '|' - соединяет два варианта описания данного разбора
  (в частности, приведения к лемме), которые считаются для участников
  конкурса одинаково допустимыми;
* круглые скобки у некоторых из альтернатив, соединяемых знаком '|' -
  обозначает тот вариант описания данного разбора, который допускается
  для участников конкурса, но не допускается для экспертов, размечающих
  Золотой стандарт (связано с допустимостью сводить видовую пару к
  единой лемме);
* квадратные скобки - обозначает тот элемент описания (внутри
  грамматической характеристики), который не является обязательным
  для участников конкурса, но должен быть включен в Золотой стандарт
  при его разметке экспертами.

При разборе формы, для которой в данных образцах использованы условные
знаки, для участников конкурса возможны различные варианты, позволяющие
получить положительную оценку:

* выбор одной из двух альтернатив, соединенных знаком '|', независимо от
  того, заключена эта альтернатива в круглые скобки или нет;
* включение или невключение информации, приводимой в Образцах в квадратных
  скобках;
* включение или невключение в поле грамматической информации
  любых других тегов, которые не совпадают ни с одним из тегов,
  упомянутых в Регламенте и Образцах.

При разметке в Золотом стандарте формы, для которой в данных образцах
использованы условные знаки, эксперты конкурса:

* при наличии альтернатив, соединенных знаком '|', необходимо сразу
  отказаться от альтернативы, заключенной в круглые скобки и осознанно
  сделать выбор из остальных;
* включить информацию, приводимую в Образцах в квадратных скобках.

"""

BASIC_TESTS = [

# ИМЯ СУЩЕСТВИТЕЛЬНОЕ
u"""
дым
    дым    S    m,sg,nom
    дым    S    m,sg,acc
дыма
    дым    S    m,sg,gen
дыму
    дым    S    m,sg,dat
    дым    S    m,sg,loc
    дым    S    m,sg[,gen2]
дымом
    дым    S    m,sg,ins
дыме
    дым    S    m,sg,loc
дымы
    дым    S    m,pl,nom
    дым    S    m,pl,acc
дымов
    дым    S    m,pl,gen
дымам
    дым    S    m,pl,dat
дымами
    дым    S    m,pl,ins
дымах
    дым    S    m,pl,loc
отче
    отец    S    m,sg[,voc]
Маш
    Маша    S    f,pl,gen
    Маша    S    f,sg[,voc]
""",

# ИМЯ ПРИЛАГАТЕЛЬНОЕ+НАРЕЧИЕ, изменяемое по степеням сравнения
u"""
тяжёлый
    тяжёлый    A    sg,m,nom
    тяжёлый    A    sg,m,acc
тяжёлого
    тяжёлый    A    sg,m,gen
    тяжёлый    A    sg,m,acc
    тяжёлый    A    sg,n,gen
тяжёлому
    тяжёлый    A    sg,m,dat
    тяжёлый    A    sg,n,dat
тяжёлым
    тяжёлый    A    sg,m,ins
    тяжёлый    A    sg,n,ins
    тяжёлый    A    pl,dat
тяжёлом
    тяжёлый    A    sg,m,loc
    тяжёлый    A    sg,n,loc
тяжёлая
    тяжёлый    A    sg,f,nom
тяжёлой
    тяжёлый    A    sg,f,gen
    тяжёлый    A    sg,f,dat
    тяжёлый    A    sg,f,ins
    тяжёлый    A    sg,f,loc
тяжёлую
    тяжёлый    A    sg,f,acc
тяжёлою
    тяжёлый    A    sg,f,ins
тяжёлое
    тяжёлый    A    sg,n,nom
    тяжёлый    A    sg,n,acc
тяжёлые
    тяжёлый    A    pl,nom
    тяжёлый    A    pl,acc
тяжёлых
    тяжёлый    A    pl,gen
    тяжёлый    A    pl,acc
    тяжёлый    A    pl,loc
тяжёлыми
    тяжёлый    A    pl,ins
тяжёл
    тяжёлый    A    sg,m[,nom][,brev]
тяжела
    тяжёлый    A    sg,f[,nom][,brev]
тяжело
    тяжёлый    A    sg,n[,nom][,brev]
    тяжело    ADV
тяжелы
    тяжёлый    A    pl[,nom][,brev]
тяжелее
    тяжёлый|(тяжелее)    A    [comp]
    тяжело|(тяжелее)    ADV    [comp]
потяжелее
    тяжёлый|(потяжелее)    A    [comp2]
    тяжело|(потяжелее)    ADV    [comp2]
тяжелейший
    тяжёлый|(тяжелейший)    A    sg,m,nom[,supr]
    тяжёлый|(тяжелейший)    A    sg,m,acc[,supr]
тяжелейшего
    тяжёлый|(тяжелейший)    A    sg,m,gen[,supr]
    тяжёлый|(тяжелейший)    A    sg,m,acc[,supr]
    тяжёлый|(тяжелейший)    A    sg,n,gen[,supr]
тяжелейшему
    тяжёлый|(тяжелейший)    A    sg,m,dat[,supr]
    тяжёлый|(тяжелейший)    A    sg,n,dat[,supr]
тяжелейшим
    тяжёлый|(тяжелейший)    A    sg,m,ins[,supr]
    тяжёлый|(тяжелейший)    A    sg,n,ins[,supr]
    тяжёлый|(тяжелейший)    A    pl,dat[,supr]
тяжелейшем
    тяжёлый|(тяжелейший)    A    sg,m,loc[,supr]
    тяжёлый|(тяжелейший)    A    sg,n,loc[,supr]
тяжелейшая
    тяжёлый|(тяжелейший)    A    sg,f,nom[,supr]
тяжелейшей
    тяжёлый|(тяжелейший)    A    sg,f,gen[,supr]
    тяжёлый|(тяжелейший)    A    sg,f,dat[,supr]
    тяжёлый|(тяжелейший)    A    sg,f,ins[,supr]
    тяжёлый|(тяжелейший)    A    sg,f,loc[,supr]
тяжелейшую
    тяжёлый|(тяжелейший)    A    sg,f,acc[,supr]
тяжелейшею
    тяжёлый|(тяжелейший)    A    sg,f,ins[,supr]
тяжелейшее
    тяжёлый|(тяжелейший)    A    sg,n,nom[,supr]
    тяжёлый|(тяжелейший)    A    sg,n,acc[,supr]
тяжелейшие
    тяжёлый|(тяжелейший)    A    pl,nom[,supr]
    тяжёлый|(тяжелейший)    A    pl,acc[,supr]
тяжелейших
    тяжёлый|(тяжелейший)    A    pl,gen[,supr]
    тяжёлый|(тяжелейший)    A    pl,acc[,supr]
    тяжёлый|(тяжелейший)    A    pl,loc[,supr]
тяжелейшими
    тяжёлый|(тяжелейший)    A    pl,ins[,supr]
тяжелейше
    тяжело|(тяжелейше)    ADV    [supr]
""",

# ГЛАГОЛ СОВЕРШЕННОГО ВИДА
# Глаголы совершенного вида, для которых соответствующий
# глагол несовершенного вида подбирается только с отбрасыванием
# (редко - присоединением) приставки (купить, порезать).
# Эти случаи трактуются как отсутствие видовой пары.
u"""
порезать
    порезать    V    inf
порежу
    порезать    V    pres,1p,sg
порежешь
    порезать    V    pres,2p,sg
порежет
    порезать    V    pres,3p,sg
порежем
    порезать    V    pres,1p,pl
    порезать    V    [imper,1p,pl]
порежете
    порезать    V    pres,2p,pl
порежут
    порезать    V    pres,3p,pl
порезав
    порезать    V    ger,past
порезавши
    порезать    V    ger,past
порезал
    порезать    V    past,m,sg
порезала
    порезать    V    past,f,sg
порезало
    порезать    V    past,n,sg
порезали
    порезать    V    past,pl
порежь
    порезать    V    imper[,2p],sg
порежьте
    порезать    V    imper[,2p],pl
порежемте
    порезать    V    [imper,1p,pl]
порезавший
    порезать    V    partcp,act,past,sg,m,nom
    порезать    V    partcp,act,past,sg,m,acc
порезавшего
    порезать    V    partcp,act,past,sg,m,gen
    порезать    V    partcp,act,past,sg,m,acc
    порезать    V    partcp,act,past,sg,n,gen
порезавшему
    порезать    V    partcp,act,past,sg,m,dat
    порезать    V    partcp,act,past,sg,n,dat
порезавшим
    порезать    V    partcp,act,past,sg,m,ins
    порезать    V    partcp,act,past,sg,n,ins
    порезать    V    partcp,act,past,pl,dat
порезавшем
    порезать    V    partcp,act,past,sg,m,loc
    порезать    V    partcp,act,past,sg,n,loc
порезавшая
    порезать    V    partcp,act,past,sg,f,nom
порезавшей
    порезать    V    partcp,act,past,sg,f,gen
    порезать    V    partcp,act,past,sg,f,dat
    порезать    V    partcp,act,past,sg,f,ins
    порезать    V    partcp,act,past,sg,f,loc
порезавшую
    порезать    V    partcp,act,past,sg,f,acc
порезавшею
    порезать    V    partcp,act,past,sg,f,ins
порезавшее
    порезать    V    partcp,act,past,sg,n,nom
    порезать    V    partcp,act,past,sg,n,acc
порезавшие
    порезать    V    partcp,act,past,pl,nom
    порезать    V    partcp,act,past,pl,acc
порезавших
    порезать    V    partcp,act,past,pl,gen
    порезать    V    partcp,act,past,pl,acc
    порезать    V    partcp,act,past,pl,loc
порезавшими
    порезать    V    partcp,act,past,pl,ins
порезаться
    порезать|порезаться    V    inf
порежусь
    порезать|порезаться    V    pres,1p,sg
порежешься
    порезать|порезаться    V    pres,2p,sg
порежется
    порезать|порезаться    V    pres,3p,sg
порежемся
    порезать|порезаться    V    pres,1p,pl
порежетесь
    порезать|порезаться    V    pres,2p,pl
порежутся
    порезать|порезаться    V    pres,3p,pl
порезавшись
    порезать|порезаться    V    ger,past
порезался
    порезать|порезаться    V    past,m,sg
порезалась
    порезать|порезаться    V    past,f,sg
порезалось
    порезать|порезаться    V    past,n,sg
порезались
    порезать|порезаться    V    past,pl
порежься
    порезать|порезаться    V    imper,2p,sg
порежьтесь
    порезать|порезаться    V    imper,2p,pl
порезанный
    порезать    V    partcp,pass,past,sg,m,nom
    порезать    V    partcp,pass,past,sg,m,acc
порезанного
    порезать    V    partcp,pass,past,sg,m,gen
    порезать    V    partcp,pass,past,sg,m,acc
    порезать    V    partcp,pass,past,sg,n,gen
порезанному
    порезать    V    partcp,pass,past,sg,m,dat
    порезать    V    partcp,pass,past,sg,n,dat
порезанным
    порезать    V    partcp,pass,past,sg,m,ins
    порезать    V    partcp,pass,past,sg,n,ins
    порезать    V    partcp,pass,past,pl,dat
порезанном
    порезать    V    partcp,pass,past,sg,m,loc
    порезать    V    partcp,pass,past,sg,n,loc
порезанная
    порезать    V    partcp,pass,past,sg,f,nom
порезанной
    порезать    V    partcp,pass,past,sg,f,gen
    порезать    V    partcp,pass,past,sg,f,dat
    порезать    V    partcp,pass,past,sg,f,ins
    порезать    V    partcp,pass,past,sg,f,loc
порезанную
    порезать    V    partcp,pass,past,sg,f,acc
порезанною
    порезать    V    partcp,pass,past,sg,f,ins
порезанное
    порезать    V    partcp,pass,past,sg,n,nom
    порезать    V    partcp,pass,past,sg,n,acc
порезанные
    порезать    V    partcp,pass,past,pl,nom
    порезать    V    partcp,pass,past,pl,acc
порезанных
    порезать    V    partcp,pass,past,pl,gen
    порезать    V    partcp,pass,past,pl,acc
    порезать    V    partcp,pass,past,pl,loc
порезанными
    порезать    V    partcp,pass,past,pl,ins
порезан
    порезать    V    partcp,pass,past,sg,m[,nom][,brev]
порезана
    порезать    V    partcp,pass,past,sg,f[,nom][,brev]
порезано
    порезать    V    partcp,pass,past,sg,n[,nom][,brev]
порезаны
    порезать    V    partcp,pass,past,pl[,nom][,brev]
порезавшийся
    порезать|порезаться    V    partcp,act,past,sg,m,nom
    порезать|порезаться    V    partcp,act,past,sg,m,acc
порезавшегося
    порезать|порезаться    V    partcp,act,past,sg,m,gen
    порезать|порезаться    V    partcp,act,past,sg,m,acc
    порезать|порезаться    V    partcp,act,past,sg,n,gen
порезавшемуся
    порезать|порезаться    V    partcp,act,past,sg,m,dat
    порезать|порезаться    V    partcp,act,past,sg,n,dat
порезавшимся
    порезать|порезаться    V    partcp,act,past,sg,m,ins
    порезать|порезаться    V    partcp,act,past,sg,n,ins
    порезать|порезаться    V    partcp,act,past,pl,dat
порезавшемся
    порезать|порезаться    V    partcp,act,past,sg,m,loc
    порезать|порезаться    V    partcp,act,past,sg,n,loc
порезавшаяся
    порезать|порезаться    V    partcp,act,past,sg,f,nom
порезавшейся
    порезать|порезаться    V    partcp,act,past,sg,f,gen
    порезать|порезаться    V    partcp,act,past,sg,f,dat
    порезать|порезаться    V    partcp,act,past,sg,f,ins
    порезать|порезаться    V    partcp,act,past,sg,f,loc
порезавшуюся
    порезать|порезаться    V    partcp,act,past,sg,f,acc
порезавшеюся
    порезать|порезаться    V    partcp,act,past,sg,f,ins
порезавшееся
    порезать|порезаться    V    partcp,act,past,sg,n,nom
    порезать|порезаться    V    partcp,act,past,sg,n,acc
порезавшиеся
    порезать|порезаться    V    partcp,act,past,pl,nom
    порезать|порезаться    V    partcp,act,past,pl,acc
порезавшихся
    порезать|порезаться    V    partcp,act,past,pl,gen
    порезать|порезаться    V    partcp,act,past,pl,acc
    порезать|порезаться    V    partcp,act,past,pl,loc
порезавшимися
    порезать|порезаться    V    partcp,act,past,pl,ins
""",

# ГЛАГОЛ НЕСОВЕРШЕННОГО ВИДА, НЕ образованный с помощью
# суффикса от глагола совершенного вида.
# Глаголы несовершенного вида, для которых соответствующий
# глагол совершенного вида подбирается только с присоединением
# (редко - отбрасыванием) приставки (резать, покупать).
# Эти случаи трактуются как отсутствие видовой пары.
u"""
читать
    читать    V    inf
читаю
    читать    V    pres,1p,sg
читаешь
    читать    V    pres,2p,sg
читает
    читать    V    pres,3p,sg
читаем
    читать    V    pres,1p,pl
    читать    V    [imper,1p,pl]
    читать    V    partcp,pass,pres,sg,m[,nom][,brev]
читаете
    читать    V    pres,2p,pl
читают
    читать    V    pres,3p,pl
читая
    читать    V    ger,pres
читав
    читать    V    ger,past
читавши
    читать    V    ger,past
читал
    читать    V    past,m,sg
читала
    читать    V    past,f,sg
читало
    читать    V    past,n,sg
читали
    читать    V    past,pl
читай
    читать    V    imper[,2p],sg
читайте
    читать    V    imper[,2p],pl
читаемте
    читать    V    [imper,1p,pl]
читающий
    читать    V    partcp,act,pres,sg,m,nom
    читать    V    partcp,act,pres,sg,m,acc
читающего
    читать    V    partcp,act,pres,sg,m,gen
    читать    V    partcp,act,pres,sg,m,acc
    читать    V    partcp,act,pres,sg,n,gen
читающему
    читать    V    partcp,act,pres,sg,m,dat
    читать    V    partcp,act,pres,sg,n,dat
читающим
    читать    V    partcp,act,pres,sg,m,ins
    читать    V    partcp,act,pres,sg,n,ins
    читать    V    partcp,act,pres,pl,dat
читающем
    читать    V    partcp,act,pres,sg,m,loc
    читать    V    partcp,act,pres,sg,n,loc
читающая
    читать    V    partcp,act,pres,sg,f,nom
читающей
    читать    V    partcp,act,pres,sg,f,gen
    читать    V    partcp,act,pres,sg,f,dat
    читать    V    partcp,act,pres,sg,f,ins
    читать    V    partcp,act,pres,sg,f,loc
читающую
    читать    V    partcp,act,pres,sg,f,acc
читающею
    читать    V    partcp,act,pres,sg,f,ins
читающее
    читать    V    partcp,act,pres,sg,n,nom
    читать    V    partcp,act,pres,sg,n,acc
читающие
    читать    V    partcp,act,pres,pl,nom
    читать    V    partcp,act,pres,pl,acc
читающих
    читать    V    partcp,act,pres,pl,gen
    читать    V    partcp,act,pres,pl,acc
    читать    V    partcp,act,pres,pl,loc
читающими
    читать    V    partcp,act,pres,pl,ins
читавший
    читать    V    partcp,act,past,sg,m,nom
    читать    V    partcp,act,past,sg,m,acc
читавшего
    читать    V    partcp,act,past,sg,m,gen
    читать    V    partcp,act,past,sg,m,acc
    читать    V    partcp,act,past,sg,n,gen
читавшему
    читать    V    partcp,act,past,sg,m,dat
    читать    V    partcp,act,past,sg,n,dat
читавшим
    читать    V    partcp,act,past,sg,m,ins
    читать    V    partcp,act,past,sg,n,ins
    читать    V    partcp,act,past,pl,dat
читавшем
    читать    V    partcp,act,past,sg,m,loc
    читать    V    partcp,act,past,sg,n,loc
читавшая
    читать    V    partcp,act,past,sg,f,nom
читавшей
    читать    V    partcp,act,past,sg,f,gen
    читать    V    partcp,act,past,sg,f,dat
    читать    V    partcp,act,past,sg,f,ins
    читать    V    partcp,act,past,sg,f,loc
читавшую
    читать    V    partcp,act,past,sg,f,acc
читавшею
    читать    V    partcp,act,past,sg,f,ins
читавшее
    читать    V    partcp,act,past,sg,n,nom
    читать    V    partcp,act,past,sg,n,acc
читавшие
    читать    V    partcp,act,past,pl,nom
    читать    V    partcp,act,past,pl,acc
читавших
    читать    V    partcp,act,past,pl,gen
    читать    V    partcp,act,past,pl,acc
    читать    V    partcp,act,past,pl,loc
читавшими
    читать    V    partcp,act,past,pl,ins
читаться
    читать|читаться    V    inf
читаюсь
    читать|читаться    V    pres,1p,sg
читаешься
    читать|читаться    V    pres,2p,sg
читается
    читать|читаться    V    pres,3p,sg
читаемся
    читать|читаться    V    pres,1p,pl
читаетесь
    читать|читаться    V    pres,2p,pl
читаются
    читать|читаться    V    pres,3p,pl
читаясь
    читать|читаться    V    ger,pres
читался
    читать|читаться    V    past,m,sg
читалась
    читать|читаться    V    past,f,sg
читалось
    читать|читаться    V    past,n,sg
читались
    читать|читаться    V    past,pl
читайся
    читать|читаться    V    imper,2p,sg
читайтесь
    читать|читаться    V    imper,2p,pl
читаемый
    читать    V    partcp,pass,pres,sg,m,nom
    читать    V    partcp,pass,pres,sg,m,acc
читаемого
    читать    V    partcp,pass,pres,sg,m,gen
    читать    V    partcp,pass,pres,sg,m,acc
    читать    V    partcp,pass,pres,sg,n,gen
читаемому
    читать    V    partcp,pass,pres,sg,m,dat
    читать    V    partcp,pass,pres,sg,n,dat
читаемым
    читать    V    partcp,pass,pres,sg,m,ins
    читать    V    partcp,pass,pres,sg,n,ins
    читать    V    partcp,pass,pres,pl,dat
читаемом
    читать    V    partcp,pass,pres,sg,m,loc
    читать    V    partcp,pass,pres,sg,n,loc
читаемая
    читать    V    partcp,pass,pres,sg,f,nom
читаемой
    читать    V    partcp,pass,pres,sg,f,gen
    читать    V    partcp,pass,pres,sg,f,dat
    читать    V    partcp,pass,pres,sg,f,ins
    читать    V    partcp,pass,pres,sg,f,loc
читаемую
    читать    V    partcp,pass,pres,sg,f,acc
читаемою
    читать    V    partcp,pass,pres,sg,f,ins
читаемое
    читать    V    partcp,pass,pres,sg,n,nom
    читать    V    partcp,pass,pres,sg,n,acc
читаемые
    читать    V    partcp,pass,pres,pl,nom
    читать    V    partcp,pass,pres,pl,acc
читаемых
    читать    V    partcp,pass,pres,pl,gen
    читать    V    partcp,pass,pres,pl,acc
    читать    V    partcp,pass,pres,pl,loc
читаемыми
    читать    V    partcp,pass,pres,pl,ins
читаема
    читать    V    partcp,pass,pres,sg,f[,nom][,brev]
читаемо
    читать    V    partcp,pass,pres,sg,n[,nom][,brev]
читаемы
    читать    V    partcp,pass,pres,pl[,nom][,brev]
читающийся
    читать|читаться    V    partcp,act,pres,sg,m,nom
    читать|читаться    V    partcp,act,pres,sg,m,acc
читающегося
    читать|читаться    V    partcp,act,pres,sg,m,gen
    читать|читаться    V    partcp,act,pres,sg,m,acc
    читать|читаться    V    partcp,act,pres,sg,n,gen
читающемуся
    читать|читаться    V    partcp,act,pres,sg,m,dat
    читать|читаться    V    partcp,act,pres,sg,n,dat
читающимся
    читать|читаться    V    partcp,act,pres,sg,m,ins
    читать|читаться    V    partcp,act,pres,sg,n,ins
    читать|читаться    V    partcp,act,pres,pl,dat
читающемся
    читать|читаться    V    partcp,act,pres,sg,m,loc
    читать|читаться    V    partcp,act,pres,sg,n,loc
читающаяся
    читать|читаться    V    partcp,act,pres,sg,f,nom
читающейся
    читать|читаться    V    partcp,act,pres,sg,f,gen
    читать|читаться    V    partcp,act,pres,sg,f,dat
    читать|читаться    V    partcp,act,pres,sg,f,ins
    читать|читаться    V    partcp,act,pres,sg,f,loc
читающуюся
    читать|читаться    V    partcp,act,pres,sg,f,acc
читающеюся
    читать|читаться    V    partcp,act,pres,sg,f,ins
читающееся
    читать|читаться    V    partcp,act,pres,sg,n,nom
    читать|читаться    V    partcp,act,pres,sg,n,acc
читающиеся
    читать|читаться    V    partcp,act,pres,pl,nom
    читать|читаться    V    partcp,act,pres,pl,acc
читающихся
    читать|читаться    V    partcp,act,pres,pl,gen
    читать|читаться    V    partcp,act,pres,pl,acc
    читать|читаться    V    partcp,act,pres,pl,loc
читающимися
    читать|читаться    V    partcp,act,pres,pl,ins
читанный
    читать    V    partcp,pass,past,sg,m,nom
    читать    V    partcp,pass,past,sg,m,acc
читанного
    читать    V    partcp,pass,past,sg,m,gen
    читать    V    partcp,pass,past,sg,m,acc
    читать    V    partcp,pass,past,sg,n,gen
читанному
    читать    V    partcp,pass,past,sg,m,dat
    читать    V    partcp,pass,past,sg,n,dat
читанным
    читать    V    partcp,pass,past,sg,m,ins
    читать    V    partcp,pass,past,sg,n,ins
    читать    V    partcp,pass,past,pl,dat
читанном
    читать    V    partcp,pass,past,sg,m,loc
    читать    V    partcp,pass,past,sg,n,loc
читанная
    читать    V    partcp,pass,past,sg,f,nom
читанной
    читать    V    partcp,pass,past,sg,f,gen
    читать    V    partcp,pass,past,sg,f,dat
    читать    V    partcp,pass,past,sg,f,ins
    читать    V    partcp,pass,past,sg,f,loc
читанную
    читать    V    partcp,pass,past,sg,f,acc
читанною
    читать    V    partcp,pass,past,sg,f,ins
читанное
    читать    V    partcp,pass,past,sg,n,nom
    читать    V    partcp,pass,past,sg,n,acc
читанные
    читать    V    partcp,pass,past,pl,nom
    читать    V    partcp,pass,past,pl,acc
читанных
    читать    V    partcp,pass,past,pl,gen
    читать    V    partcp,pass,past,pl,acc
    читать    V    partcp,pass,past,pl,loc
читанными
    читать    V    partcp,pass,past,pl,ins
читан
    читать    V    partcp,pass,past,sg,m[,nom][,brev]
читана
    читать    V    partcp,pass,past,sg,f[,nom][,brev]
читано
    читать    V    partcp,pass,past,sg,n[,nom][,brev]
читаны
    читать    V    partcp,pass,past,pl[,nom][,brev]
читавшийся
    читать|читаться    V    partcp,act,past,sg,m,nom
    читать|читаться    V    partcp,act,past,sg,m,acc
читавшегося
    читать|читаться    V    partcp,act,past,sg,m,gen
    читать|читаться    V    partcp,act,past,sg,m,acc
    читать|читаться    V    partcp,act,past,sg,n,gen
читавшемуся
    читать|читаться    V    partcp,act,past,sg,m,dat
    читать|читаться    V    partcp,act,past,sg,n,dat
читавшимся
    читать|читаться    V    partcp,act,past,sg,m,ins
    читать|читаться    V    partcp,act,past,sg,n,ins
    читать|читаться    V    partcp,act,past,pl,dat
читавшемся
    читать|читаться    V    partcp,act,past,sg,m,loc
    читать|читаться    V    partcp,act,past,sg,n,loc
читавшаяся
    читать|читаться    V    partcp,act,past,sg,f,nom
читавшейся
    читать|читаться    V    partcp,act,past,sg,f,gen
    читать|читаться    V    partcp,act,past,sg,f,dat
    читать|читаться    V    partcp,act,past,sg,f,ins
    читать|читаться    V    partcp,act,past,sg,f,loc
читавшуюся
    читать|читаться    V    partcp,act,past,sg,f,acc
читавшеюся
    читать|читаться    V    partcp,act,past,sg,f,ins
читавшееся
    читать|читаться    V    partcp,act,past,sg,n,nom
    читать|читаться    V    partcp,act,past,sg,n,acc
читавшиеся
    читать|читаться    V    partcp,act,past,pl,nom
    читать|читаться    V    partcp,act,past,pl,acc
читавшихся
    читать|читаться    V    partcp,act,past,pl,gen
    читать|читаться    V    partcp,act,past,pl,acc
    читать|читаться    V    partcp,act,past,pl,loc
читавшимися
    читать|читаться    V    partcp,act,past,pl,ins
""",

# ГЛАГОЛ СОВЕРШЕННОГО ВИДА, от которого с помощью суффикса может быть
# образован глагол несовершенного вида
# Глаголы совершенного вида, для которых соответствующий глагол
# несовершенного вида может быть образован без участия приставок
# (решить - решать, поднять - поднимать, съесть - съедать)
u"""
решить
    решить|(решать)    V    inf
решу
    решить|(решать)    V    pres,1p,sg
решишь
    решить|(решать)    V    pres,2p,sg
решит
    решить|(решать)    V    pres,3p,sg
решим
    решить|(решать)    V    pres,1p,pl
    решить|(решать)    V    [imper,1p,pl]
решите
    решить|(решать)    V    pres,2p,pl
решат
    решить|(решать)    V    pres,3p,pl
решив
    решить|(решать)    V    ger,past
решивши
    решить|(решать)    V    ger,past
решил
    решить|(решать)    V    past,m,sg
решила
    решить|(решать)    V    past,f,sg
решило
    решить|(решать)    V    past,n,sg
решили
    решить|(решать)    V    past,pl
реши
    решить|(решать)    V    imper[,2p],sg
решите
    решить|(решать)    V    imper[,2p],pl
решимте
    решить|(решать)    V    [imper,1p,pl]
решивший
    решить|(решать)    V    partcp,act,past,sg,m,nom
    решить|(решать)    V    partcp,act,past,sg,m,acc
решившего
    решить|(решать)    V    partcp,act,past,sg,m,gen
    решить|(решать)    V    partcp,act,past,sg,m,acc
    решить|(решать)    V    partcp,act,past,sg,n,gen
решившему
    решить|(решать)    V    partcp,act,past,sg,m,dat
    решить|(решать)    V    partcp,act,past,sg,n,dat
решившим
    решить|(решать)    V    partcp,act,past,sg,m,ins
    решить|(решать)    V    partcp,act,past,sg,n,ins
    решить|(решать)    V    partcp,act,past,pl,dat
решившем
    решить|(решать)    V    partcp,act,past,sg,m,loc
    решить|(решать)    V    partcp,act,past,sg,n,loc
решившая
    решить|(решать)    V    partcp,act,past,sg,f,nom
решившей
    решить|(решать)    V    partcp,act,past,sg,f,gen
    решить|(решать)    V    partcp,act,past,sg,f,dat
    решить|(решать)    V    partcp,act,past,sg,f,ins
    решить|(решать)    V    partcp,act,past,sg,f,loc
решившую
    решить|(решать)    V    partcp,act,past,sg,f,acc
решившею
    решить|(решать)    V    partcp,act,past,sg,f,ins
решившее
    решить|(решать)    V    partcp,act,past,sg,n,nom
    решить|(решать)    V    partcp,act,past,sg,n,acc
решившие
    решить|(решать)    V    partcp,act,past,pl,nom
    решить|(решать)    V    partcp,act,past,pl,acc
решивших
    решить|(решать)    V    partcp,act,past,pl,gen
    решить|(решать)    V    partcp,act,past,pl,acc
    решить|(решать)    V    partcp,act,past,pl,loc
решившими
    решить|(решать)    V    partcp,act,past,pl,ins
решиться
    решить|решиться|(решать)|(решаться)    V    inf
решусь
    решить|решиться|(решать)|(решаться)    V    pres,1p,sg
решишься
    решить|решиться|(решать)|(решаться)    V    pres,2p,sg
решится
    решить|решиться|(решать)|(решаться)    V    pres,3p,sg
решимся
    решить|решиться|(решать)|(решаться)    V    pres,1p,pl
решитесь
    решить|решиться|(решать)|(решаться)    V    pres,2p,pl
решатся
    решить|решиться|(решать)|(решаться)    V    pres,3p,pl
решившись
    решить|решиться|(решать)|(решаться)    V    ger,pres
решась
    решить|решиться|(решать)|(решаться)    V    ger,pres
решился
    решить|решиться|(решать)|(решаться)    V    past,m,sg
решилась
    решить|решиться|(решать)|(решаться)    V    past,f,sg
решилось
    решить|решиться|(решать)|(решаться)    V    past,n,sg
решились
    решить|решиться|(решать)|(решаться)    V    past,pl
решись
    решить|решиться|(решать)|(решаться)    V    imper,2p,sg
решитесь
    решить|решиться|(решать)|(решаться)    V    imper,2p,pl
решённый
    решить|(решать)    V    partcp,pass,past,sg,m,nom
    решить|(решать)    V    partcp,pass,past,sg,m,acc
решённого
    решить|(решать)    V    partcp,pass,past,sg,m,gen
    решить|(решать)    V    partcp,pass,past,sg,m,acc
    решить|(решать)    V    partcp,pass,past,sg,n,gen
решённому
    решить|(решать)    V    partcp,pass,past,sg,m,dat
    решить|(решать)    V    partcp,pass,past,sg,n,dat
решённым
    решить|(решать)    V    partcp,pass,past,sg,m,ins
    решить|(решать)    V    partcp,pass,past,sg,n,ins
    решить|(решать)    V    partcp,pass,past,pl,dat
решённом
    решить|(решать)    V    partcp,pass,past,sg,m,loc
    решить|(решать)    V    partcp,pass,past,sg,n,loc
решённая
    решить|(решать)    V    partcp,pass,past,sg,f,nom
решённой
    решить|(решать)    V    partcp,pass,past,sg,f,gen
    решить|(решать)    V    partcp,pass,past,sg,f,dat
    решить|(решать)    V    partcp,pass,past,sg,f,ins
    решить|(решать)    V    partcp,pass,past,sg,f,loc
решённую
    решить|(решать)    V    partcp,pass,past,sg,f,acc
решённою
    решить|(решать)    V    partcp,pass,past,sg,f,ins
решённое
    решить|(решать)    V    partcp,pass,past,sg,n,nom
    решить|(решать)    V    partcp,pass,past,sg,n,acc
решённые
    решить|(решать)    V    partcp,pass,past,pl,nom
    решить|(решать)    V    partcp,pass,past,pl,acc
решённых
    решить|(решать)    V    partcp,pass,past,pl,gen
    решить|(решать)    V    partcp,pass,past,pl,acc
    решить|(решать)    V    partcp,pass,past,pl,loc
решёнными
    решить|(решать)    V    partcp,pass,past,pl,ins
решён
    решить|(решать)    V    partcp,pass,past,sg,m[,nom][,brev]
решена
    решить|(решать)    V    partcp,pass,past,sg,f[,nom][,brev]
решено
    решить|(решать)    V    partcp,pass,past,sg,n[,nom][,brev]
решены
    решить|(решать)    V    partcp,pass,past,pl[,nom][,brev]
решившийся
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,m,nom
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,m,acc
решившегося
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,m,gen
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,m,acc
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,n,gen
решившемуся
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,m,dat
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,n,dat
решившимся
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,m,ins
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,n,ins
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,pl,dat
решившемся
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,m,loc
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,n,loc
решившаяся
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,f,nom
решившейся
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,f,gen
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,f,dat
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,f,ins
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,f,loc
решившуюся
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,f,acc
решившеюся
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,f,ins
решившееся
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,n,nom
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,sg,n,acc
решившиеся
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,pl,nom
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,pl,acc
решившихся
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,pl,gen
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,pl,acc
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,pl,loc
решившимися
    решить|решиться|(решать)|(решаться)    V    partcp,act,past,pl,ins
""",

# ГЛАГОЛ НЕСОВЕРШЕННОГО ВИДА, образованный с помощью суффикса от глагола
# совершенного вида
# Глаголы несовершенного вида, для которых соответствующий глагол
# совершенного вида может быть образован без участия приставок
# (решать - решить, поднимать - поднять, съедать - съесть).
u"""
решать
    решать|(решить)    V    inf
решаю
    решать|(решить)    V    pres,1p,sg
решаешь
    решать|(решить)    V    pres,2p,sg
решает
    решать|(решить)    V    pres,3p,sg
решаем
    решать|(решить)    V    pres,1p,pl
    решать|(решить)    V    [imper,1p,pl]
    решать|(решить)    V    partcp,pass,pres,sg,m[,nom][,brev]
решаете
    решать|(решить)    V    pres,2p,pl
решают
    решать|(решить)    V    pres,3p,pl
решая
    решать|(решить)    V    ger,pres
решал
    решать|(решить)    V    past,m,sg
решала
    решать|(решить)    V    past,f,sg
решало
    решать|(решить)    V    past,n,sg
решали
    решать|(решить)    V    past,pl
решай
    решать|(решить)    V    imper[,2p],sg
решайте
    решать|(решить)    V    imper[,2p],pl
решаемте
    решать|(решить)    V    [imper,1p,pl]
решающий
    решать|(решить)    V    partcp,act,pres,sg,m,nom
    решать|(решить)    V    partcp,act,pres,sg,m,acc
решающего
    решать|(решить)    V    partcp,act,pres,sg,m,gen
    решать|(решить)    V    partcp,act,pres,sg,m,acc
    решать|(решить)    V    partcp,act,pres,sg,n,gen
решающему
    решать|(решить)    V    partcp,act,pres,sg,m,dat
    решать|(решить)    V    partcp,act,pres,sg,n,dat
решающим
    решать|(решить)    V    partcp,act,pres,sg,m,ins
    решать|(решить)    V    partcp,act,pres,sg,n,ins
    решать|(решить)    V    partcp,act,pres,pl,dat
решающем
    решать|(решить)    V    partcp,act,pres,sg,m,loc
    решать|(решить)    V    partcp,act,pres,sg,n,loc
решающая
    решать|(решить)    V    partcp,act,pres,sg,f,nom
решающей
    решать|(решить)    V    partcp,act,pres,sg,f,gen
    решать|(решить)    V    partcp,act,pres,sg,f,dat
    решать|(решить)    V    partcp,act,pres,sg,f,ins
    решать|(решить)    V    partcp,act,pres,sg,f,loc
решающую
    решать|(решить)    V    partcp,act,pres,sg,f,acc
решающею
    решать|(решить)    V    partcp,act,pres,sg,f,ins
решающее
    решать|(решить)    V    partcp,act,pres,sg,n,nom
    решать|(решить)    V    partcp,act,pres,sg,n,acc
решающие
    решать|(решить)    V    partcp,act,pres,pl,nom
    решать|(решить)    V    partcp,act,pres,pl,acc
решающих
    решать|(решить)    V    partcp,act,pres,pl,gen
    решать|(решить)    V    partcp,act,pres,pl,acc
    решать|(решить)    V    partcp,act,pres,pl,loc
решающими
    решать|(решить)    V    partcp,act,pres,pl,ins
решавший
    решать|(решить)    V    partcp,act,past,sg,m,nom
    решать|(решить)    V    partcp,act,past,sg,m,acc
решавшего
    решать|(решить)    V    partcp,act,past,sg,m,gen
    решать|(решить)    V    partcp,act,past,sg,m,acc
    решать|(решить)    V    partcp,act,past,sg,n,gen
решавшему
    решать|(решить)    V    partcp,act,past,sg,m,dat
    решать|(решить)    V    partcp,act,past,sg,n,dat
решавшим
    решать|(решить)    V    partcp,act,past,sg,m,ins
    решать|(решить)    V    partcp,act,past,sg,n,ins
    решать|(решить)    V    partcp,act,past,pl,dat
решавшем
    решать|(решить)    V    partcp,act,past,sg,m,loc
    решать|(решить)    V    partcp,act,past,sg,n,loc
решавшая
    решать|(решить)    V    partcp,act,past,sg,f,nom
решавшей
    решать|(решить)    V    partcp,act,past,sg,f,gen
    решать|(решить)    V    partcp,act,past,sg,f,dat
    решать|(решить)    V    partcp,act,past,sg,f,ins
    решать|(решить)    V    partcp,act,past,sg,f,loc
решавшую
    решать|(решить)    V    partcp,act,past,sg,f,acc
решавшею
    решать|(решить)    V    partcp,act,past,sg,f,ins
решавшее
    решать|(решить)    V    partcp,act,past,sg,n,nom
    решать|(решить)    V    partcp,act,past,sg,n,acc
решавшие
    решать|(решить)    V    partcp,act,past,pl,nom
    решать|(решить)    V    partcp,act,past,pl,acc
решавших
    решать|(решить)    V    partcp,act,past,pl,gen
    решать|(решить)    V    partcp,act,past,pl,acc
    решать|(решить)    V    partcp,act,past,pl,loc
решавшими
    решать|(решить)    V    partcp,act,past,pl,ins
решаться
    решать|решаться|(решить)|(решиться)    V    inf
решаюсь
    решать|решаться|(решить)|(решиться)    V    pres,1p,sg
решаешься
    решать|решаться|(решить)|(решиться)    V    pres,2p,sg
решается
    решать|решаться|(решить)|(решиться)    V    pres,3p,sg
решаемся
    решать|решаться|(решить)|(решиться)    V    pres,1p,pl
решаетесь
    решать|решаться|(решить)|(решиться)    V    pres,2p,pl
решаются
    решать|решаться|(решить)|(решиться)    V    pres,3p,pl
решаясь
    решать|решаться|(решить)|(решиться)    V    ger,pres
решался
    решать|решаться|(решить)|(решиться)    V    past,m,sg
решалась
    решать|решаться|(решить)|(решиться)    V    past,f,sg
решалось
    решать|решаться|(решить)|(решиться)    V    past,n,sg
решались
    решать|решаться|(решить)|(решиться)    V    past,pl
решайся
    решать|решаться|(решить)|(решиться)    V    imper,2p,sg
решайтесь
    решать|решаться|(решить)|(решиться)    V    imper,2p,pl
решаемый
    решать|(решить)    V    partcp,pass,pres,sg,m,nom
    решать|(решить)    V    partcp,pass,pres,sg,m,acc
решаемого
    решать|(решить)    V    partcp,pass,pres,sg,m,gen
    решать|(решить)    V    partcp,pass,pres,sg,m,acc
    решать|(решить)    V    partcp,pass,pres,sg,n,gen
решаемому
    решать|(решить)    V    partcp,pass,pres,sg,m,dat
    решать|(решить)    V    partcp,pass,pres,sg,n,dat
решаемым
    решать|(решить)    V    partcp,pass,pres,sg,m,ins
    решать|(решить)    V    partcp,pass,pres,sg,n,ins
    решать|(решить)    V    partcp,pass,pres,pl,dat
решаемом
    решать|(решить)    V    partcp,pass,pres,sg,m,loc
    решать|(решить)    V    partcp,pass,pres,sg,n,loc
решаемая
    решать|(решить)    V    partcp,pass,pres,sg,f,nom
решаемой
    решать|(решить)    V    partcp,pass,pres,sg,f,gen
    решать|(решить)    V    partcp,pass,pres,sg,f,dat
    решать|(решить)    V    partcp,pass,pres,sg,f,ins
    решать|(решить)    V    partcp,pass,pres,sg,f,loc
решаемую
    решать|(решить)    V    partcp,pass,pres,sg,f,acc
решаемою
    решать|(решить)    V    partcp,pass,pres,sg,f,ins
решаемое
    решать|(решить)    V    partcp,pass,pres,sg,n,nom
    решать|(решить)    V    partcp,pass,pres,sg,n,acc
решаемые
    решать|(решить)    V    partcp,pass,pres,pl,nom
    решать|(решить)    V    partcp,pass,pres,pl,acc
решаемых
    решать|(решить)    V    partcp,pass,pres,pl,gen
    решать|(решить)    V    partcp,pass,pres,pl,acc
    решать|(решить)    V    partcp,pass,pres,pl,loc
решаемыми
    решать|(решить)    V    partcp,pass,pres,pl,ins
решаема
    решать|(решить)    V    partcp,pass,pres,sg,f[,nom][,brev]
решаемо
    решать|(решить)    V    partcp,pass,pres,sg,n[,nom][,brev]
решаемы
    решать|(решить)    V    partcp,pass,pres,pl[,nom][,brev]
решающийся
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,m,nom
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,m,acc
решающегося
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,m,gen
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,m,acc
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,n,gen
решающемуся
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,m,dat
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,n,dat
решающимся
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,m,ins
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,n,ins
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,pl,dat
решающемся
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,m,loc
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,n,loc
решающаяся
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,f,nom
решающейся
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,f,gen
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,f,dat
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,f,ins
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,f,loc
решающуюся
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,f,acc
решающеюся
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,f,ins
решающееся
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,n,nom
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,sg,n,acc
решающиеся
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,pl,nom
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,pl,acc
решающихся
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,pl,gen
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,pl,acc
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,pl,loc
решающимися
    решать|решаться|(решить)|(решиться)    V    partcp,act,pres,pl,ins
решавшийся
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,m,nom
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,m,acc
решавшегося
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,m,gen
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,m,acc
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,n,gen
решавшемуся
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,m,dat
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,n,dat
решавшимся
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,m,ins
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,n,ins
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,pl,dat
решавшемся
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,m,loc
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,n,loc
решавшаяся
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,f,nom
решавшейся
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,f,gen
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,f,dat
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,f,ins
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,f,loc
решавшуюся
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,f,acc
решавшеюся
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,f,ins
решавшееся
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,n,nom
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,sg,n,acc
решавшиеся
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,pl,nom
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,pl,acc
решавшихся
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,pl,gen
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,pl,acc
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,pl,loc
решавшимися
    решать|решаться|(решить)|(решиться)    V    partcp,act,past,pl,ins
""",
]
