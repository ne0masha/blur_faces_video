# Используем официальный образ Python
FROM python:3.12-slim

# Указываем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
# Устанавливаем зависимости
RUN pip install --upgrade pip -r requirements.txt

# Копируем все файлы в контейнер
COPY . /app

# Указываем команду для запуска
EXPOSE 5000
