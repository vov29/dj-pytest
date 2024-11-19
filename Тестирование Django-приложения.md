# Тестирование Django-приложения  
**import** pytest  
**from** model\_bakery **import** baker  
**from** rest\_framework.test **import** APIClient

**from** students.models **import** Course

@pytest.fixture  
**def** ***api\_client***():  
    **return** APIClient()

@pytest.fixture  
**def** ***course\_factory***():  
    **def** ***factory***(\*\*kwargs):  
        **return** baker.make(Course, \*\*kwargs)  
    **return** factory

@pytest.fixture  
**def** ***student\_factory***():  
    **def** ***factory***(\*\*kwargs):  
        **return** baker.make('students.Student', \*\*kwargs)  
    **return** factory

@pytest.mark.django\_db  
**def** ***test\_retrieve\_course***(api\_client, course\_factory):  
    course \= course\_factory(name="Test Course")  
    url \= f"/api/v1/courses/{course.id}/"  
    response \= api\_client.get(url)  
    **assert** response.status\_code \== 200  
    **assert** response.data\['name'\] \== "Test Course"

@pytest.mark.django\_db  
**def** ***test\_list\_courses***(api\_client, course\_factory):  
    course\_factory(name="Course 1")  
    course\_factory(name="Course 2")  
    response \= api\_client.get("/api/v1/courses/")  
    **assert** response.status\_code \== 200  
    **assert** len(response.data) \== 2

@pytest.mark.django\_db  
**def** ***test\_filter\_courses\_by\_id***(api\_client, course\_factory):  
    course1 \= course\_factory(name="Course 1", id\=1)  
    course\_factory(name="Course 2", id\=2)  
    response \= api\_client.get("/api/v1/courses/", data={'id': course1.id})  
    **assert** response.status\_code \== 200  
    **assert** len(response.data) \== 1  
    **assert** response.data\[0\]\['id'\] \== course1.id

@pytest.mark.django\_db  
**def** ***test\_filter\_courses\_by\_name***(api\_client, course\_factory):  
    course\_factory(name="Course 1")  
    course2 \= course\_factory(name="Course 2")  
    response \= api\_client.get("/api/v1/courses/", data={'name': course2.name})  
    **assert** response.status\_code \== 200  
    **assert** len(response.data) \== 1  
    **assert** response.data\[0\]\['name'\] \== course2.name

@pytest.mark.django\_db  
**def** ***test\_create\_course***(api\_client):  
    data \= {'name': 'New Course'}  
    response \= api\_client.post("/api/v1/courses/", data=data, format\='json')  
    **assert** response.status\_code \== 201  
    **assert** response.data\['name'\] \== 'New Course'

@pytest.mark.django\_db  
**def** ***test\_update\_course***(api\_client, course\_factory):  
    course \= course\_factory(name="Old Course")  
    data \= {'name': 'Updated Course'}  
    url \= f"/api/v1/courses/{course.id}/"  
    response \= api\_client.patch(url, data=data, format\='json')  
    **assert** response.status\_code \== 200  
    **assert** response.data\['name'\] \== 'Updated Course'

@pytest.mark.django\_db  
**def** ***test\_delete\_course***(api\_client, course\_factory):  
    course \= course\_factory()  
    url \= f"/api/v1/courses/{course.id}/"  
    response \= api\_client.delete(url)  
    **assert** response.status\_code \== 204

# Этот код предполагает, что у Вас уже настроен проект Django с необходимыми моделями, сериализаторами, представлениями и URL-адресами, как показано в предоставленных Вами фрагментах кода. Перед запуском тестов убедитесь, что Вы установили pytest и model-bakery: pip install pytest model-bakery и выполнили необходимые миграции базы данных. Также убедитесь, что Ваша база данных PostgreSQL запущена и доступна. Запуск тестов осуществляется командой pytest.


## Этот код представляет собой набор тестов для Django REST Framework API, который управляет курсами. Он должен быть размещен в файле tests/students/test\_courses\_api.py (или аналогичном, в зависимости от Вашей структуры проекта). Разберем код по частям:

1\. Импорты:

**import** pytest  
**from** model\_bakery **import** baker  
**from** rest\_framework.test **import** APIClient  
**from** students.models **import** Course

* pytest: Фреймворк для написания тестов.  
* model\_bakery: Библиотека для создания тестовых данных (фикстур).  
* rest\_framework.test.APIClient: Клиент для отправки запросов к API.  
* students.models import Course: Импорт модели Course из приложения students.

2\. Фикстуры:

@pytest.fixture  
**def** ***api\_client***():  
    **return** APIClient()

@pytest.fixture  
**def** ***course\_factory***():  
    **def** ***factory***(\*\*kwargs):  
        **return** baker.make(Course, \*\*kwargs)  
    **return** factory

@pytest.fixture  
**def** ***student\_factory***():  
    **def** ***factory***(\*\*kwargs):  
        **return** baker.make('students.Student', \*\*kwargs)  
    **return** factory

* api\_client: Создает экземпляр APIClient для использования в тестах. Это позволяет отправлять HTTP-запросы к API.  
* course\_factory: "Фабрика" для создания объектов Course с помощью model\_bakery. \*\*kwargs позволяет создавать курсы с различными атрибутами.  
* student\_factory: Аналогично, фабрика для создания объектов Student. 'students.Student' указывает на модель студента, предполагая, что она находится в приложении students.

3\. Тест-кейсы:

Каждый из последующих методов – это отдельный тест-кейс. Все они используют декоратор @pytest.mark.django\_db, который гарантирует, что каждый тест выполняется в рамках транзакции с базой данных, и изменения, внесенные во время теста, отменяются после его завершения.

* test\_retrieve\_course: Проверяет получение одного курса по его ID.  
* test\_list\_courses: Проверяет получение списка всех курсов.  
* test\_filter\_courses\_by\_id: Проверяет фильтрацию курсов по ID.  
* test\_filter\_courses\_by\_name: Проверяет фильтрацию курсов по имени.  
* test\_create\_course: Проверяет создание нового курса.  
* test\_update\_course: Проверяет обновление существующего курса.  
* test\_delete\_course: Проверяет удаление курса.

Пример одного тест-кейса (test\_retrieve\_course):

@pytest.mark.django\_db  
**def** ***test\_retrieve\_course***(api\_client, course\_factory):  
    course \= course\_factory(name="Test Course")  \# Создаем курс с помощью фабрики  
    url \= f"/api/v1/courses/{course.id}/"       \# Формируем URL  
    response \= api\_client.get(url)              \# Отправляем GET-запрос  
    **assert** response.status\_code \== 200          \# Проверяем код ответа (200 \- OK)  
    **assert** response.data\['name'\] \== "Test Course" \# Проверяем, что имя курса соответствует

## Как добавить код в проект:

1. Создайте файл test\_courses\_api.py: Внутри директории tests/students/ (или аналогичной) Вашего Django проекта создайте файл с именем test\_courses\_api.py.  
2. Вставьте код: Скопируйте и вставьте весь предоставленный код в этот файл.  
3. Запустите тесты: В терминале, находясь в корневой директории Вашего проекта, выполните команду pytest.

Важно: Убедитесь, что у Вас установлены необходимые библиотеки (pytest и model\_bakery), а также что Ваши модели (Course и Student), сериализаторы, представления и URL-адреса настроены корректно. В противном случае тесты могут не пройти или выдать ошибки. Помните, что для успешного выполнения тестов, Ваша база данных должна быть настроена и запущена. В settings.py убедитесь, что DATABASES указывает на корректную конфигурацию PostgreSQL.

## Ошибка django.core.exceptions.ImproperlyConfigured: Requested setting INSTALLED\_APPS, but settings are not configured означает, что model\_bakery (а через нее и Ваши тесты) пытается обратиться к настройкам Django, прежде чем они были правильно инициализированы. Это типичная проблема при запуске тестов Django вне контекста Django-сервера.

Решение заключается в явном указании Django, какие настройки использовать для запуска тестов. Это делается с помощью pytest-django.

1\. Установите pytest-django:

pip install pytest-django

2\. Модифицируйте Ваши тесты: Вам нужно будет сообщить pytest-django, где найти Ваши настройки Django. Есть несколько способов сделать это:

* Через команду pytest: Вы можете указать путь к настройкам с помощью флага \--ds (или \--django-settings-module). Замените django\_testing.settings на имя Вашего файла настроек.

pytest \--ds=django\_testing.settings

*   
* Через файл conftest.py (Рекомендуемый подход): Создайте файл conftest.py в корневой директории Вашего тестового пакета (на одном уровне с test\_courses\_api.py). В этом файле добавьте следующую строку:  
* PythonКопировать

**import** pytest  
pytest\_plugins \= \['pytester'\]

django\_db\_setup \= **True**

**def** ***pytest\_configure***(config):  
    config.option.django\_settings\_module \= "django\_testing.settings"

* Этот метод предпочтительнее, потому что он делает настройки более явными и не требует дополнительных аргументов при запуске pytest.

3\. Убедитесь, что INSTALLED\_APPS в settings.py корректен:

Проверьте, что в Вашем файле settings.py в INSTALLED\_APPS указано приложение students и все необходимые приложения Django (например, rest\_framework, django\_filters).

4\. (Возможно) Удалите или прокомментируйте django\_db\_setup \= True:

Если у Вас есть django\_db\_setup \= True в conftest.py, попробуйте его удалить или закомментировать. pytest-django сам управляет базой данных в тестах с @pytest.mark.django\_db.

После внесения этих изменений:

* Запустите pytest (с флагом \--ds или через conftest.py).  
* Если ошибка сохраняется, внимательно изучите предупреждения, которые выдает pytest – они могут указывать на другие проблемы в конфигурации проекта.

В целом, использование pytest-django — лучший и наиболее надежный способ запуска тестов Django. Он автоматизирует многие шаги и предотвращает подобные проблемы с конфигурацией.

## Есть два способа запустить pytest после внесения изменений, описанных в предыдущем ответе:

Метод 1: Использование флага \--ds (или \--django-settings-module)

1. Откройте командную строку или терминал. Перейдите в корневой каталог Вашего проекта Django (там, где находится файл manage.py).  
2. Запустите pytest с флагом \--ds: Замените django\_testing.settings на фактическое имя Вашего файла настроек Django (обычно settings.py, но может быть и другим, если Вы его переименовали).

pytest \--ds\=django\_testing.settings

3. или, более длинная версия:

pytest \--django-settings-module=django\_testing.settings


Метод 2: Использование conftest.py

1. Создайте файл conftest.py: Если его ещё нет, создайте файл conftest.py в той же директории, где находятся Ваши файлы тестов (например, tests/). Вставьте в него код:

**import** pytest  
pytest\_plugins \= \['pytester'\]  \#Это строчка может быть не нужна.   
django\_db\_setup \= **True** \# эту строку можно закомментировать или удалить.

**def** ***pytest\_configure***(config):  
    config.option.django\_settings\_module \= "django\_testing.settings"

2. Замените "django\_testing.settings" на путь к Вашему файлу настроек Django, если он находится в другом месте. Например, если он находится в папке my\_app, то нужно написать "my\_app.settings".  
3. Запустите pytest: Теперь Вы можете запустить pytest без дополнительных флагов:

pytest

pytest автоматически обнаружит и использует conftest.py, настроенный для использования Ваших настроек Django.

Какой метод лучше?

Метод с использованием conftest.py предпочтительнее, так как он делает настройку более явной частью Вашего проекта и не требует дополнительных аргументов при каждом запуске тестов. Это делает процесс более воспроизводимым и менее подверженным ошибкам. Если Вы используете систему контроля версий (Git), настройки в conftest.py будут храниться вместе с вашими тестами.

