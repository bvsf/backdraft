#!/bin/sh

ssh root@srv-backdraft <<EOF
  cd backdraft
  git pull
  source /backdraft/venv/bin/activate
  pip install -r requirements.txt
  ./manage.py migrate
  sudo supervisorctl restart backdraft
  exit
EOF