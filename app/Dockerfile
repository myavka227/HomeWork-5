FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости для сборки uwsgi и psycopg2
# Мы объединяем установку и очистку кеша в один слой, чтобы образ был меньше
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Сначала копируем только requirements, чтобы использовать кеш слоев Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

CMD ["uwsgi", "--ini", "uwsgi.ini"]