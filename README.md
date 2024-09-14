# Homework_24

### Фильтрация для вывода курсов и уроков
- Примеры запросов: http://127.0.0.1:8000/api/lms
- /lessons/ - Список и создание уроков через LessonListCreateAPIView.
- /lessons/<id>/ - Получение, обновление и удаление уроков через 
- /courses/ - lessons_count Возвращает количество уроков для каждого курса. lessons возвращает уроки курса


### Фильтрация для вывода списка платежей с возможностями:
- Примеры запросов: http://127.0.0.1:8000/api/users 
- /payments/?ordering=date - Сортировка по дате оплаты (по возрастанию)
- /payments/?ordering=-date - Сортировка по дате оплаты (по убыванию)
- /payments/?course=1 - фильтрация по курсу
- /payments/?lesson=3 - Фильтрация по уроку
- /payments/?payment_method=cash - Фильтрация по способу оплаты

### Вывод истории платежей пользователя
- Примеры запросов: http://127.0.0.1:8000/api/users/
- /profile/{id}/ - Профиль пользователя по id с полем
- profile/ - Профиль пользователя
- list/ - Профили пользователей
- detail/{id}/ - Платежи данного пользователя
- register/ - Регистрация пользователя 
- token/ - Получение токена
- token/refresh/ - Продление токена
- profile/{id}/ -Просмотр профиля пользователя


Группа модераторов "Moderators" может работать с любыми уроками и курсами, но без возможности их удалять и создавать новые.
Пользователи, которые не входят в группу модераторов, могут видеть, редактировать и удалять только свои курсы и уроки.



# Проект Django с Celery, PostgreSQL и Redis в Docker

Этот проект представляет собой веб-приложение на Django с использованием Celery для
асинхронных задач, PostgreSQL в качестве базы данных и Redis как брокера сообщений.
Все компоненты работают внутри Docker-контейнеров для упрощения настройки и развертывания.

## Структура проекта

- `web`: контейнер с Django-приложением.
- `db`: контейнер базы данных PostgreSQL.
- `redis`: контейнер Redis для брокера сообщений Celery.

## Установка и запуск проекта


```bash
git clone https://github.com/GSmagin/Homework_24.git
cd Homework_24

2. Создайте файл .env
Создайте файл .env в корне проекта и добавьте, заполните параметры из .env.example

3. Запуск контейнеров
Чтобы собрать и запустить контейнеры, выполните команду:

docker-compose up --build
Это команда создаст и запустит контейнеры для Django, PostgreSQL и Redis.

4. Применение миграций
После запуска контейнеров необходимо применить миграции базы данных:

docker-compose exec web python manage.py migrate
5. Создание суперпользователя
Создайте суперпользователя для доступа к административной панели Django:

docker-compose exec web python manage.py createsuperuser
6. Запуск Celery
Для запуска Celery worker и Celery beat выполните следующие команды в отдельных терминалах:

docker-compose exec web celery -A confing worker --loglevel=info

docker-compose exec web celery -A confing beat --loglevel=info

7. Доступ к приложению
После успешного запуска всех контейнеров приложение будет доступно по адресу http://localhost:8008.

Админка Django доступна по адресу http://localhost:8008/admin.

Полезные команды
Остановка контейнеров:

docker-compose down
Сборка данных в JSON:

docker-compose exec web python manage.py dumpdata > db_backup.json
Восстановление данных из JSON:

docker-compose exec web python manage.py loaddata db_backup.json