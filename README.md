booking_hotel
Простой сервис для управления номерами отелей и их бронированиями (Django, DRF, PostgreSQL).

Стек технологий
Python 3.10+
Django
Django REST Framework
PostgreSQL
Docker, docker-compose
pytest
Быстрый старт
Клонировать репозиторий

git clone <your_repo_url>
cd booking_hotel
Создать и заполнить .env

POSTGRES_USER=main
POSTGRES_PASSWORD=1234
POSTGRES_DB=booking
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
Создать базу данных booking в PostgreSQL вручную (через pgAdmin или psql).

Установить зависимости

poetry install
Выполнить миграции

python manage.py makemigrations
python manage.py migrate
Запустить сервер

python manage.py runserver
или через Docker:

docker-compose up --build
Примеры запросов
Номера отеля
Добавить номер

curl -X POST -d "description=Супер номер" -d "price_per_night=3000" http://localhost:8000/rooms/create/
Ответ: {"room_id": 1}

Удалить номер

curl -X DELETE http://localhost:8000/rooms/delete/1/
Список номеров

curl -X GET "http://localhost:8000/rooms/list/?sort_by=price&order=desc"
Бронирования
Добавить бронь

curl -X POST -d "room=1" -d "date_start=2024-06-10" -d "date_end=2024-06-12" http://localhost:8000/bookings/create/
Ответ: {"booking_id": 2}

Удалить бронь

curl -X DELETE http://localhost:8000/bookings/delete/2/
Список броней номера

curl -X GET "http://localhost:8000/bookings/list/?room_id=1"
Принятые решения
Проверка пересечений дат реализована на уровне сериализатора Booking.
Все ошибки возвращаются в формате JSON.
Без авторизации.
Данные не теряются между перезагрузками (используется PostgreSQL).
Сортировка номеров реализована по цене и дате добавления.
Вопросы/замечания
Если потребуется авторизация — легко добавить через DRF.
Для production рекомендуется вынести секретные ключи в .env и использовать защищённые переменные окружения.