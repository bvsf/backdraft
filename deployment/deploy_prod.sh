#!/bin/sh

# https://rahmonov.me/posts/continuous-integration-and-continous-deployment-for-django-app-with-jenkins/

  cd backdraft
  git pull .
  source venv/bin/activate
  pip install -r requirements.txt
  python manage.py migrate
  python manage.py runserver
  # sudo supervisorctl restart backdraft
  exit