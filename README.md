# comments_checker
Скрипт является консольной программой для автоматизации поиска нецензурных слов, оскорблений, политических высказываний и пр. в комментариях к статьям на одном очень известном интернет ресурсе.

## Использование

В каталоге [dicts](https://github.com/igorzakhar/comments-checker/tree/main/dicts) данного репозитория находятся текстовые файлы со списками слов, которые нужно распознавать. Слова можно объеденить в одном файле или разбить на несколько файлов по определенным тематикам. При запуске скрипта слова из всех файлов объединяются в единый список. Дальше, текст комментариев проверятся на наличие слов из этого "черного списка". Перед проверкой из комментария удаляются знаки препинание и прочая пунктуация, слова приводятся к нормальному виду.

Пример запуска:
```bash
$ python comments_checker.py https://habr.com/ru/articles/785516/
...
→ https://habr.com/ru/articles/785516/comments/#comment_26365166
Главное отличие XP и Win7 от Win8/8/10/11 - они были простыми из коробки и в них не было ничего лишнего. Чего-о-о? Как старпёр, который переползал еще  3.1 на 3.11 (+ почти с десяток дискет!) могу вас заверить, что в момент выхода и ХP была страшным тормозящим пропроитарным неповоротливым прожорливым монстром.  Она плохо поддерживала оборудование (как я намучился со звуковухой!), жрала 56 кбитный интернет, как не в себя. Ей не хватало 100 Мб жёсткого диска! Мне пришлось Civilization 2 удалять, чтоб место освободить! Вы представляете? И эта тварь ещё  смела привязываться к железу , $#%@ ! Это тогда было просто немыслимое наступление на мои "свободы пользователя"!  А от этого детско-мультяшного интерфеса вообще тошнило. И куча всякой ненужной фигни (уж извините - уже и забылось от чего тогда кипелось). Не,  XP приобрела "человеческое лицо" только на SP3.   Это Vista и семёрка (да-да, семёрка!) сделали эту систему "святой" теми ужасами, что они принесли ...
Detected words: ['тварь', 'старпер']
----------------------------------------
→ https://habr.com/ru/articles/785516/comments/#comment_26365398
 И эта тварь ещё  смела привязываться к железу   Standard IDE controller. Постоянно устанавливал его перед перенесом на другое железо
Detected words: ['тварь']
----------------------------------------

```


## Зависимости

Для запуска скрипта использовался только Python 3.8, на других версиях не проверялся.

Рекомендуется устанавливать зависимости в виртуальном окружении, используя [venv](https://docs.python.org/3/library/venv.html) или любую другую реализацию, например, [virtualenv](https://github.com/pypa/virtualenv).

В примере используется модуль `venv` который появился в стандартной библиотеке python версии 3.3.

1. Скопируйте репозиторий в текущий каталог. Воспользуйтесь командой:
```bash
$ git clone https://github.com/igorzakhar/comments-checker.git
```

После этого программа будет скопирована в каталог `comments-checker`.

2. Создайте и активируйте виртуальное окружение:
```bash
$ cd comments-checker # Переходим в каталог с программой
$ python3 -m venv my_virtual_environment # Создаем виртуальное окружение
$ source my_virtual_environment/bin/activate # Активируем виртуальное окружение
```

3. Установите сторонние библиотеки  из файла зависимостей:
```bash
$ pip install -r requirements.txt # В качестве альтернативы используйте pip3
```
