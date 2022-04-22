
release: python manage.py makemigrations
release: python manage.py migrate
web:gunicorn ExpenseTrackerApi.wsgi --log-file -