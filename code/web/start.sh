#!/bin/bash


#source "$VENV_PATH/bin/activate"

export FLASK_APP=app.py
export FLASK_ENV=production
export PYTHONUNBUFFERED=1

nohup gunicorn app:app --bind 0.0.0.0:5000 --workers 2 --threads 4 --timeout 120 > server.log 2>&1 &
