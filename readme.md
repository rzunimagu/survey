## Подготовка проекта для запуска
Для запуска проекта, необходимы установленные **docker** и **docker-compose**

Сборка проекта: 
```
docker-compose build survey
```

Создание всех необходимых таблиц в БД: 
```
docker-compose run survey python manage.py migrate
```

Создание пользователя с правами админа 
```
docker-compose run survey python manage.py createsuperuser
```

Запуск: 
```
docker-compose run survey
```

После запуска проект будет доступен по адресу 
```
http://127.0.0.1:8000/
```

## Адреса для api
### login:
```
http://127.0.0.1:8000/auth/login
```
### Функционал администратора

#### работа с опросами
```
GET http://127.0.0.1:8000/api/admin/polls/ - список доступных опросов
POST http://127.0.0.1:8000/api/admin/polls/ - добавить опрос
GET http://127.0.0.1:8000/api/admin/polls/<int: id>/ - информация об опросе с указанным id
PUT http://127.0.0.1:8000/api/admin/polls/<int: id>/ - обновить информацию об опросе 
DELETE http://127.0.0.1:8000/api/admin/polls/<int: id>/ - удалить опрос
```

#### Редактирование вопросов
```
GET http://127.0.0.1:8000/api/admin/polls/<int: poll_id>/questions/ - список вопросов у выбранного опросника
POST http://127.0.0.1:8000/api/admin/polls/<int: poll_id>/questions/ - добавить вопрос
GET http://127.0.0.1:8000/api/admin/polls/<int: poll_id>/questions/<int: question_id>/ - информация о выбранном вопросе
PUT http://127.0.0.1:8000/api/admin/polls/<int: poll_id>/questions/<int: question_id>/ - изменить вопрос
DELETE http://127.0.0.1:8000/api/admin/polls/<int: poll_id>/questions/<int: question_id>/ - удалить вопрос
```

#### Редактирование вариантов ответа для вопроса
Добавлять варианты ответа можно как непосредственно при редактировании опроса, 
но так же доступны и отдельные роуты для них. Роуты доступны только для опросов у которых подразумевается выбор одного 
или нескольких вариантов.
```
GET http://127.0.0.1:8000/api/admin/polls/<int: poll_id>/questions/<int: question_id>/options/ - список вариантов ответа 
POST http://127.0.0.1:8000/api/admin/polls/<int: poll_id>/questions/<int: question_id>/options/ - добавить вариант 
PUT http://127.0.0.1:8000/api/admin/polls/<int: poll_id>/questions/<int: question_id>/options/<int: options_id>/ - изменить вариант
DELETE http://127.0.0.1:8000/api/admin/polls/<int: poll_id>/questions/<int: question_id>/options/<int: options_id>/ - удалить вариант
```

### Общедоступный функционал

#### Активные опросы    
```
GET http://127.0.0.1:8000/api/user/active-polls/ - полный список активных опросов
GET http://127.0.0.1:8000/api/user/active-polls/<int: poll_id>/ - информация об опросе  
POST http://127.0.0.1:8000/api/user/active-polls/<int: poll_id>/questions/<int: question_id> - ответить на вопрос
```
#### Результаты пользователя    
```
GET http://127.0.0.1:8000/api/user/results/ - результаты пользователей
GET http://127.0.0.1:8000/api/user/results/<int: user_id> - результаты конкретного пользователя
```


## Задача: спроектировать и разработать API для системы опросов пользователей.

### Функционал для администратора системы:

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

### Функционал для пользователей системы:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Использовать следующие технологии: Django, Django REST framework.

### Результат выполнения задачи:
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по разворачиванию приложения (в docker или локально)
- документация по API
