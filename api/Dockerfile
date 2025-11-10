FROM python:3.10-slim

# working dir inside container
WORKDIR /app

# system deps for psycopg2 etc.
RUN apt-get update && apt-get install -y libpq-dev build-essential && rm -rf /var/lib/apt/lists/*

# install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy source code
COPY . .

ENV PYTHONUNBUFFERED=1

# ENTRYPOINT script that checks/creates project & app
CMD bash -c '\
if [ ! -f manage.py ]; then \
  echo "==> Creating Django project backend"; \
  django-admin startproject backend .; \
fi && \
if [ ! -d emails ]; then \
  echo "==> Creating Django app emails"; \
  python manage.py startapp emails; \
fi && \
echo "==> Running migrations"; \
python manage.py migrate --noinput && \
echo "==> Starting server at 0.0.0.0:8000"; \
python manage.py runserver 0.0.0.0:8000'
