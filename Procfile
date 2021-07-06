release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn allremont.wsgi
web: python allremont/manage.py runserver 0.0.0.0:$PORT
