FROM python:3.9-slim

WORKDIR /code

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       libjpeg-dev \
       zlib1g-dev \
       libmagic1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

# Collect static files during build (optional, can also be done in entrypoint.sh)
# RUN python manage.py collectstatic --noinput

# Default command (overridden by docker-compose)
CMD ["gunicorn", "petrosanattaraz.wsgi:application", "--bind", "0.0.0.0:8000"]
