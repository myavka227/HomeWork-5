FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir Flask Flask-SQLAlchemy psycopg2-binary redis uwsgi Flask-Migrate

COPY . .

CMD ["uwsgi", "--ini", "uwsgi.ini"]