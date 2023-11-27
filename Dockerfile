# Использование базового образа с поддержкой PyTorch
FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime

# Установка рабочей директории
WORKDIR /app

# Создание и активация виртуальной среды
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Копирование файла зависимостей в контейнер
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов проекта
COPY . .

# Определение команды для запуска приложения
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
