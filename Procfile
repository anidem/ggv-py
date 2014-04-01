# Procfile for heroku deployment
web: python manage.py collectstatic --noinput --verbosity 0 --settings=ggvproject.settings.prod ; gunicorn ggvproject.wsgi
