#!/bin/sh

PROJECT_NAME="backend"
APPS="users emails"

cd /app

# 1️⃣ Create Django project if missing
if [ ! -f "/app/manage.py" ]; then
  echo "📁 No Django project found. Creating project '$PROJECT_NAME'..."
  django-admin startproject $PROJECT_NAME .
fi

# 2️⃣ Create apps if missing
for app in $APPS; do
  if [ ! -d "/app/$app" ]; then
    echo "🛠 Creating app '$app'..."
    python manage.py startapp $app
  fi
done

# 3️⃣ Make migrations for all apps
echo "📦 Making migrations..."
python manage.py makemigrations $APPS

# 4️⃣ Apply migrations
echo "📦 Applying migrations..."
python manage.py migrate --noinput

# 5️⃣ Create superuser if not exists
echo "👑 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin','admin@example.com','adminpass')
"

# 6️⃣ Start Django server
echo "🚀 Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
