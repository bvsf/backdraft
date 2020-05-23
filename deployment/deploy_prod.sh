#!/bin/sh

# https://rahmonov.me/posts/continuous-integration-and-continous-deployment-for-django-app-with-jenkins/

  cd backdraft
  git pull .
  source venv/bin/activate
  pip install -r requirements.txt
  ./manage.py migrate
  # sudo supervisorctl restart backdraft
  exit