
# Используем официальный образ Python (замените версию на нужную, 3.13 используется в вопросе)
FROM python:3.13-slim

# 1. Установка системных зависимостей (для компиляции и работы БД)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    libpq-dev postgresql-client \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Установка Poetry
RUN pip install --no-cache-dir poetry==1.5.1

# 3. Настройка рабочей директории
WORKDIR /app

# 4. Копирование файлов зависимостей и Poetry-локов для установки
COPY pyproject.toml poetry.lock* /app/

# 5. Установка зависимостей через Poetry (с отключением создания venv)
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# 6. Копирование остального кода проекта
COPY . /app/

# 7. Переменные окружения (опционально: для корректной работы Python)
ENV PYTHONUNBUFFERED=1  PYTHONDONTWRITEBYTECODE=1

# 8. Запуск приложения (через poetry, который запустит manage.py)
# В данном случае команда запуска переопределяется в docker-compose,
# но можно оставить на случай прямого docker run:
CMD ["poetry", "run", "python", "booking_hotel/manage.py", "runserver", "0.0.0.0:8000"]
