# Проект по БД

Получает данные о компаниях и вакансиях с сайта [hh.ru](https://hh.ru/) , создается БД и таблицы в PostgreSQL и загружаются полученные данные в созданные таблицы

Инструкции по установке
------------
1. Клонировать репозиторий
   ```sh
   git clone https://github.com/MarinaKrasnoruzhskaya/course_work_4.git
   ```
2. Установить Poetry
   ```sh
   pip install poetry
   ```
3. Инициализировать Poetry
   ```sh
   poetry init
   ```
4. Установить зависимости
   ```sh
   poetry install
   ```
5. Обновить зависимости
   ```sh
   poetry update
   ```
6. В корне проекта создать файл database.ini и ввести данные для работы с PostgreSQL
   ```sh
   [postgresql]
   host=
   user=
   password=
   port=
   ```
7. В файле ```data\companies.json``` изменить или оставить без изменения представленный список ```Работодателей``` и их ```id``` на [hh.ru](https://hh.ru/) 

<p align="right">(<a href="#readme-top">Наверх</a>)</p>


Руководство по использованию
---------------
1. После запуска main.pу, выполняется парсинг 10 работодателей из файла ```data\companies.json``` и их вакансий с платформы hh.ru 
2. Полученные данные записываются в созданную БД ```hh``` в две связанные таблицы ```employers``` и ```vacancies```
3. Выполняются запросы на выборку и фильтрацию данных в PostgreSQL, результаты запросов будут выведена в консоли или записана в csv файлы в зависимости от объёма выводимой информации  

Контакты
---------------
Марина Красноружская - krasnoruzhskayamarina@yandex.ru

Ссылка на проект: [https://github.com/MarinaKrasnoruzhskaya/course_work_5.git](https://github.com/MarinaKrasnoruzhskaya/course_work_5.git)