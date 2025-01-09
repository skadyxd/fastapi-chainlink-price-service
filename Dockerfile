FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Экспортируем переменную окружения для указания переменной FastAPI
ENV PYTHONUNBUFFERED=1

# Команда запуска Uvicorn сервера
CMD ["uvicorn", "app.main:app_fastapi", "--host", "0.0.0.0", "--port", "8000"]